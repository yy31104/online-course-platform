# Django Online Course Application (Full Project Overview)

This repository contains a full Django online course system built through the IBM Full Stack learning path, including:

- user authentication (registration/login/logout)
- course catalog and enrollment
- course detail pages with lesson content
- exam/assessment workflow (question -> choice -> submission -> scoring)
- Django admin management for course content
- Bootstrap-based UI templates

## Project Scope

This is **not only a final-lab patch**. The repository includes the complete app flow from earlier labs to final assessment features:

1. Base online course data model and course browsing
2. Function-based and class-based/generic views
3. Authentication and user enrollment flow
4. Bootstrap integration for course pages
5. Assessment system (Question/Choice/Submission)
6. Exam submission and result evaluation

## Tech Stack

- Python
- Django 4.2.3
- SQLite (default local database)
- Bootstrap 4.5.2 (CDN)
- Pillow (image support)

## Repository Structure

```text
.
©À©¤©¤ manage.py
©À©¤©¤ myproject/
©¦   ©À©¤©¤ settings.py
©¦   ©À©¤©¤ urls.py
©¦   ©¸©¤©¤ wsgi.py
©À©¤©¤ onlinecourse/
©¦   ©À©¤©¤ admin.py
©¦   ©À©¤©¤ models.py
©¦   ©À©¤©¤ urls.py
©¦   ©À©¤©¤ views.py
©¦   ©À©¤©¤ migrations/
©¦   ©¸©¤©¤ templates/onlinecourse/
©¦       ©À©¤©¤ course_list_bootstrap.html
©¦       ©À©¤©¤ course_detail_bootstrap.html
©¦       ©À©¤©¤ exam_result_bootstrap.html
©¦       ©À©¤©¤ user_login_bootstrap.html
©¦       ©¸©¤©¤ user_registration_bootstrap.html
©¸©¤©¤ static/
```

## Core Domain Models

Defined in `onlinecourse/models.py`.

- `Instructor`: linked to Django `User`, tracks teaching profile
- `Learner`: linked to Django `User`, stores learner profile
- `Course`: course metadata, image, instructors, enrolled users
- `Lesson`: one-to-many under `Course`
- `Enrollment`: bridge between `User` and `Course`
- `Question`: exam question under `Course`, includes grade points
- `Choice`: options under `Question`, includes correctness flag
- `Submission`: one exam attempt, linked to `Enrollment`, many-to-many with `Choice`

### Assessment Scoring Rule

`Question.is_get_score(selected_ids)` gives score only when:

- all correct choices are selected
- no incorrect choices are selected

So each question is exact-match scoring.

## Main User Flows

### 1. Browse and Enroll

- User visits `/onlinecourse/`
- Sees top courses ordered by enrollment
- Clicks `Enroll` -> enrollment record created (if authenticated)

### 2. Learn and Take Exam

- User enters course detail page
- Lessons are displayed first
- Exam section renders all questions and choices
- User submits selected answers

### 3. View Exam Result

- System creates `Submission`
- Selected choices are recorded
- Score is calculated question-by-question
- Result page displays:
  - pass/fail message
  - grade percentage
  - per-question scoring details
  - selected/correct choice highlights

## URL Map

From `myproject/urls.py` and `onlinecourse/urls.py`:

- `/admin/` - Django admin
- `/onlinecourse/` - course list (home)
- `/onlinecourse/registration/` - register
- `/onlinecourse/login/` - login
- `/onlinecourse/logout/` - logout
- `/onlinecourse/<pk>/` - course detail
- `/onlinecourse/<course_id>/enroll/` - enroll
- `/onlinecourse/<course_id>/submit/` - submit exam
- `/onlinecourse/<course_id>/submission/<submission_id>/` - exam result

## Local Run (Windows)

Use Python 3.11 for best compatibility with this project setup.

```powershell
cd "C:\×ÀÃæ\IBM FullStack\SQL\Add a New Assessment Feature to an Online Course Application\tfjzl-final-cloud-app-with-database"

# Create and activate virtualenv
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

## Admin Setup and Test Data

1. Create a superuser:

```powershell
python manage.py createsuperuser
```

2. Login to admin and create:

- Instructor (bind a user)
- Course (with image + instructors)
- Lessons for the course
- Questions for the course
- Choices for each question (mark correct options)

3. Enroll from frontend and submit exam to validate scoring.

## Final Assessment Feature (What Was Added in Final Task)

The final lab enhancement includes:

- new models: `Question`, `Choice`, `Submission`
- admin inlines for question/choice editing
- exam block added to course detail template
- `submit` view and `show_exam_result` view
- corresponding URL routes
- exam result Bootstrap template with pass/fail UX

## Common Issues

### Admin crash: `'super' object has no attribute 'dicts'`

This is typically a Python runtime compatibility issue (commonly Python 3.14 with old dependency combinations in this lab context).

Fix:

- use Python 3.11 virtualenv
- reinstall dependencies inside the new venv
- rerun `migrate` and `runserver`

### Course images not showing

Check:

- image file exists under `static/media/course_images/`
- `MEDIA_URL` and `MEDIA_ROOT` are configured
- `urlpatterns` include `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`

## Submission Artifacts (AI-Graded)

If you are submitting the lab for grading, keep these artifacts ready:

- public GitHub repo URL
- `03-admin-site` screenshot
- `07-final` screenshot
- code in models/admin/views/urls/templates aligned with rubric

## License

Apache-2.0 (see `LICENSE`)
