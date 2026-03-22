from django.contrib import messages
from django.contrib.auth import login, logout
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .forms import LoginForm, RegistrationForm
from .models import Choice, Course, Enrollment, Submission
from .services import calculate_submission_result, extract_selected_choice_ids


def registration_request(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome to the platform.")
            return redirect("onlinecourse:index")
        messages.error(request, "Please fix the highlighted fields and try again.")
    else:
        form = RegistrationForm()

    return render(
        request,
        "onlinecourse/user_registration_bootstrap.html",
        {"form": form},
    )


def login_request(request):
    if request.user.is_authenticated:
        return redirect("onlinecourse:index")

    next_url = request.GET.get("next", request.POST.get("next", ""))
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "You are now logged in.")
            return redirect(next_url or "onlinecourse:index")
        messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm(request)

    return render(
        request,
        "onlinecourse/user_login_bootstrap.html",
        {"form": form, "next": next_url},
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("onlinecourse:index")


def check_if_enrolled(user, course):
    if not user.is_authenticated:
        return False
    return Enrollment.objects.filter(user=user, course=course).exists()


class CourseListView(generic.ListView):
    template_name = "onlinecourse/course_list_bootstrap.html"
    context_object_name = "course_list"

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by("-total_enrollment")[:10]
        enrolled_course_ids = set()
        if user.is_authenticated:
            enrolled_course_ids = set(
                Enrollment.objects.filter(user=user, course__in=courses).values_list(
                    "course_id",
                    flat=True,
                )
            )
        for course in courses:
            course.is_enrolled = course.id in enrolled_course_ids
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "onlinecourse/course_detail_bootstrap.html"

    def get_queryset(self):
        return Course.objects.prefetch_related("lesson_set", "question_set__choice_set")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        context["is_enrolled"] = check_if_enrolled(self.request.user, course)
        context["lessons"] = course.lesson_set.order_by("order")
        context["questions"] = course.question_set.prefetch_related("choice_set")
        return context


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if not user.is_authenticated:
        messages.info(request, "Please login before enrolling.")
        login_url = reverse("onlinecourse:login")
        return redirect(f"{login_url}?next={request.path}")

    with transaction.atomic():
        _, created = Enrollment.objects.get_or_create(
            user=user,
            course=course,
            defaults={"mode": Enrollment.HONOR},
        )
        if created:
            Course.objects.filter(pk=course.pk).update(
                total_enrollment=F("total_enrollment") + 1
            )
            messages.success(request, f"You are enrolled in {course.name}.")
        else:
            messages.info(request, "You are already enrolled in this course.")

    return HttpResponseRedirect(
        reverse(viewname="onlinecourse:course_details", args=(course.id,))
    )


def submit(request, course_id):
    if request.method != "POST":
        messages.warning(request, "Assessment submissions must use POST.")
        return redirect("onlinecourse:course_details", pk=course_id)

    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if not user.is_authenticated:
        messages.info(request, "Please login to submit the assessment.")
        login_url = reverse("onlinecourse:login")
        return redirect(f"{login_url}?next={request.path}")

    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    selected_choice_ids = extract_selected_choice_ids(request.POST)
    if not selected_choice_ids:
        messages.warning(request, "Select at least one choice before submitting.")
        return redirect("onlinecourse:course_details", pk=course_id)

    selected_choices = Choice.objects.filter(
        id__in=selected_choice_ids,
        question__course=course,
    )
    if not selected_choices.exists():
        messages.warning(request, "No valid answer choices were found for this assessment.")
        return redirect("onlinecourse:course_details", pk=course_id)

    with transaction.atomic():
        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.add(*selected_choices)

    return HttpResponseRedirect(
        reverse(
            viewname="onlinecourse:show_exam_result",
            args=(course.id, submission.id),
        )
    )


def show_exam_result(request, course_id, submission_id):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to view assessment results.")
        login_url = reverse("onlinecourse:login")
        return redirect(f"{login_url}?next={request.path}")

    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__course=course,
        enrollment__user=request.user,
    )

    result_payload = calculate_submission_result(course, submission)
    context = {
        "course": course,
        "submission": submission,
        **result_payload,
    }
    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
