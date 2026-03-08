# Django Online Course Application

This repository contains a full Django online course platform built across multiple lab stages, including authentication, course enrollment, lesson delivery, and exam assessment.

## What This Project Includes

- User registration, login, and logout
- Course list and enrollment workflow
- Course detail pages with lessons
- Exam workflow with questions and choices
- Exam submission and score evaluation
- Django admin management for content creation
- Bootstrap based UI templates

## Tech Stack

- Python
- Django 4.2.3
- SQLite
- Bootstrap 4.5.2
- Pillow

## Repository Structure

```text
.
|-- manage.py
|-- myproject/
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- onlinecourse/
|   |-- admin.py
|   |-- models.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- templates/onlinecourse/
|       |-- course_list_bootstrap.html
|       |-- course_detail_bootstrap.html
|       |-- exam_result_bootstrap.html
|       |-- user_login_bootstrap.html
|       `-- user_registration_bootstrap.html
|-- static/
|-- requirements.txt
|-- runtime.txt
|-- Procfile
`-- manifest.yml
```

## Core Models

Defined in `onlinecourse/models.py`:

- `Instructor`
- `Learner`
- `Course`
- `Lesson`
- `Enrollment`
- `Question`
- `Choice`
- `Submission`

## Main Application Flow

1. User opens `/onlinecourse/` and browses courses.
2. User enrolls in a course.
3. User reads lessons in the course detail page.
4. User starts exam and submits answers.
5. System creates `Submission`, evaluates answers, and returns result page.

## URL Reference

- `/admin/`
- `/onlinecourse/`
- `/onlinecourse/registration/`
- `/onlinecourse/login/`
- `/onlinecourse/logout/`
- `/onlinecourse/<pk>/`
- `/onlinecourse/<course_id>/enroll/`
- `/onlinecourse/<course_id>/submit/`
- `/onlinecourse/<course_id>/submission/<submission_id>/`

## Local Setup (Windows)

Use Python 3.11 for this project.

```powershell
cd <your-local-path>\tfjzl-final-cloud-app-with-database

py -3.11 -m venv .venv311
.\.venv311\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

- App: `http://127.0.0.1:8000/onlinecourse/`
- Admin: `http://127.0.0.1:8000/admin/`

## Admin Setup

Create admin user:

```powershell
python manage.py createsuperuser
```

Then in Django admin, create data in this order:

1. Instructor (bind to an existing user)
2. Course
3. Lesson
4. Question
5. Choice

## Assessment Scoring Logic

`Question.is_get_score(selected_ids)` gives full points only when:

- all correct choices are selected
- no incorrect choices are selected

This is exact match scoring per question.

## Final Enhancement Summary

Final stage additions:

- Added models: `Question`, `Choice`, `Submission`
- Added admin inlines for question and choice editing
- Added exam form on course detail template
- Added `submit` and `show_exam_result` views
- Added routes for submit and result pages
- Added Bootstrap based exam result UI

## Troubleshooting

### Admin error: `'super' object has no attribute 'dicts'`

This usually happens with Python 3.14 in this lab setup.

Fix:

1. Create a Python 3.11 virtual environment
2. Reinstall dependencies
3. Run migrations again
4. Restart server

### Media not displayed

Check:

- `MEDIA_URL` and `MEDIA_ROOT` are configured
- `urlpatterns` include media static mapping in development
- image files exist under `static/media/`

## License

Apache-2.0. See `LICENSE`.
