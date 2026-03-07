# Add a New Assessment Feature to an Online Course Application

This repository contains my completion of the IBM Skills Network final Django lab:

- Added assessment models: `Question`, `Choice`, `Submission`
- Registered new models and inlines in Django admin
- Added course exam UI in `course_detail_bootstrap.html`
- Implemented exam submission and result flow in `views.py`
- Added routes for `submit` and `show_exam_result`
- Completed Bootstrap exam result template

## Repository

- GitHub: `https://github.com/yy31104/tfjzl-final-cloud-app-with-database`

## Local Run (Windows)

Use **Python 3.11** (recommended for Django 4.2.x compatibility).

```powershell
cd "C:\桌面\IBM FullStack\SQL\Add a New Assessment Feature to an Online Course Application\tfjzl-final-cloud-app-with-database"

# Optional: create a Python 3.11 virtual environment
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

## If You See Admin Error: `'super' object has no attribute 'dicts'`

This usually means Python runtime incompatibility (commonly Python 3.14 with Django 4.2.x).
Switch to Python 3.11 virtualenv and rerun.

## What Was Committed

1. `feat(models): add assessment models and initial migration`
   - `onlinecourse/models.py`
   - `onlinecourse/migrations/0001_initial.py`

2. `feat(admin): register assessment models and inlines`
   - `onlinecourse/admin.py`

3. `feat(exam): add submit flow, exam result view, routes and templates`
   - `onlinecourse/views.py`
   - `onlinecourse/urls.py`
   - `onlinecourse/templates/onlinecourse/course_detail_bootstrap.html`
   - `onlinecourse/templates/onlinecourse/exam_result_bootstrap.html`

4. `docs: update README and ignore local .venv311`
   - `README.md`
   - `.gitignore`

## AI-Graded Submission Checklist

- `03-admin-site` screenshot: Django admin showing both sections:
  - `AUTHENTICATION AND AUTHORIZATION`
  - `ONLINECOURSE`
- `07-final` screenshot: successful exam attempt with:
  - Congratulations message
  - score
  - exam results list
- Public GitHub repo URL above
