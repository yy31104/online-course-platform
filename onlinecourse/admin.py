from django.contrib import admin

from .models import (
    Choice,
    Course,
    Enrollment,
    Instructor,
    Learner,
    Lesson,
    Question,
    Submission,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ("name", "pub_date", "total_enrollment")
    list_filter = ("pub_date",)
    search_fields = ("name", "description")
    ordering = ("name",)
    readonly_fields = ("total_enrollment",)
    fieldsets = (
        ("Basic Info", {"fields": ("name", "description", "image", "pub_date")}),
        ("People and Metrics", {"fields": ("instructors", "total_enrollment")}),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "content")
    ordering = ("course", "order")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "course", "grade")
    list_filter = ("course",)
    search_fields = ("question_text",)
    ordering = ("course",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")
    list_filter = ("is_correct", "question__course")
    search_fields = ("choice_text", "question__question_text")
    ordering = ("question",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "mode", "rating", "date_enrolled")
    list_filter = ("mode", "date_enrolled", "course")
    search_fields = ("user__username", "course__name")
    autocomplete_fields = ("user", "course")
    ordering = ("-date_enrolled",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "enrollment", "submitted_at")
    list_filter = ("submitted_at", "enrollment__course")
    search_fields = ("enrollment__user__username", "enrollment__course__name")
    autocomplete_fields = ("enrollment",)
    ordering = ("-submitted_at",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")
    list_filter = ("full_time",)
    search_fields = ("user__username",)
    autocomplete_fields = ("user",)


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation", "social_link")
    list_filter = ("occupation",)
    search_fields = ("user__username", "social_link")
    autocomplete_fields = ("user",)
