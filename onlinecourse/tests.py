from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Course, Enrollment, Question, Submission
from .services import calculate_submission_result, extract_selected_choice_ids


def create_test_image():
    return SimpleUploadedFile(
        "test_course.gif",
        (
            b"GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
            b"\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
            b"\x00\x02\x02D\x01\x00;"
        ),
        content_type="image/gif",
    )


class OnlineCourseWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.other_user = User.objects.create_user(username="bob", password="pass1234")
        self.course = Course.objects.create(
            name="Django Fundamentals",
            image=create_test_image(),
            description="Core Django course",
        )
        self.question = Question.objects.create(
            course=self.course,
            question_text="Which choices are correct?",
            grade=5,
        )
        self.correct_choice = Choice.objects.create(
            question=self.question,
            choice_text="Correct option",
            is_correct=True,
        )
        self.wrong_choice = Choice.objects.create(
            question=self.question,
            choice_text="Wrong option",
            is_correct=False,
        )

    def test_extract_selected_choice_ids(self):
        post_data = {
            "choice1": "11",
            "choice2": "12",
            "non_choice": "ignore",
        }
        self.assertEqual(extract_selected_choice_ids(post_data), [11, 12])

    def test_calculate_submission_result_exact_match(self):
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.add(self.correct_choice)

        result = calculate_submission_result(self.course, submission)

        self.assertEqual(result["total_score"], 5)
        self.assertEqual(result["total_possible"], 5)
        self.assertEqual(result["grade"], 100)

    def test_enroll_does_not_duplicate_or_overcount(self):
        self.client.login(username="alice", password="pass1234")
        enroll_url = reverse("onlinecourse:enroll", args=(self.course.id,))

        self.client.post(enroll_url)
        self.client.post(enroll_url)

        self.assertEqual(
            Enrollment.objects.filter(user=self.user, course=self.course).count(),
            1,
        )
        self.course.refresh_from_db()
        self.assertEqual(self.course.total_enrollment, 1)

    def test_submit_requires_selected_choice(self):
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        self.client.login(username="alice", password="pass1234")
        submit_url = reverse("onlinecourse:submit", args=(self.course.id,))

        response = self.client.post(submit_url, {})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Submission.objects.filter(enrollment=enrollment).count(),
            0,
        )

    def test_result_page_restricted_to_submission_owner(self):
        enrollment_owner = Enrollment.objects.create(user=self.user, course=self.course)
        submission = Submission.objects.create(enrollment=enrollment_owner)
        submission.choices.add(self.correct_choice)

        self.client.login(username="bob", password="pass1234")
        result_url = reverse(
            "onlinecourse:show_exam_result",
            args=(self.course.id, submission.id),
        )
        response = self.client.get(result_url)

        self.assertEqual(response.status_code, 404)
