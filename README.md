# Task Management System (Django + DRF)

A production-style Task Manager backend built with Django and Django REST Framework.
This project supports JWT auth, task lifecycle management, filtering/search, comments,
attachments, dashboard analytics, demo access flows, and Vercel deployment.

## Live Demo

- App URL: `https://task-management-system-izdeb35vg-maloth-sridhar-varmas-projects.vercel.app/`
- One-click admin demo: `GET /api/auth/demo-admin/`
- JWT demo user login: `POST /api/auth/demo-login/`

## Features

### Core (MVP)
- User registration, JWT login, token refresh, logout with token blacklist
- Task CRUD (create, list, retrieve, update, delete)
- Task fields: `title`, `description`, `priority`, `status`, `due_date`
- Filtering by `status`, `priority`, `due_date`
- Search by task `title` and `description`
- Overdue logic (`is_overdue`) for unfinished tasks past due date
- Dashboard counts (`total`, `completed`, `overdue`, `due_today`, etc.)

### Nice-to-Have
- Task comments
- File attachments
- Email reminder command for due/overdue tasks
- Demo Admin one-click login to Django Admin panel
- Demo User JWT button from landing page

## Tech Stack

- Python 3.12
- Django 6
- Django REST Framework
- SimpleJWT (`djangorestframework-simplejwt`)
- `django-filter`
- PostgreSQL (Neon)
- WhiteNoise (static files on Vercel)
- Vercel deployment

## Project Structure

```text
task-manager-django/
  accounts/
    urls.py
    views.py
    serializers.py
  config/
    settings.py
    urls.py
  tasks/
    models.py
    views.py
    serializers.py
    urls.py
    management/commands/send_due_task_reminders.py
  requirements.txt
  vercel.json
  manage.py
```

## Database Tables

### `tasks_task`
- `id` (PK)
- `user_id` (FK -> auth_user)
- `title`
- `description`
- `status` (`todo`, `in_progress`, `done`)
- `priority` (`low`, `medium`, `high`)
- `due_date`
- `attachment`
- `reminder_sent`
- `created_at`
- `updated_at`

### `tasks_taskcomment`
- `id` (PK)
- `task_id` (FK -> tasks_task)
- `user_id` (FK -> auth_user)
- `comment`
- `created_at`

### JWT Blacklist Tables
- `token_blacklist_outstandingtoken`
- `token_blacklist_blacklistedtoken`

## API Endpoints

### Auth
- `POST /api/auth/register/` - Register user
- `POST /api/auth/login/` - Login and get access/refresh tokens
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Blacklist refresh token
- `POST /api/auth/demo-login/` - Demo User JWT login
- `GET /api/auth/demo-admin/` - Session login as Demo Admin and redirect to `/admin/`

### Tasks
- `GET /api/tasks/` - List current user tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Task details
- `PUT/PATCH /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/tasks/dashboard/` - Dashboard analytics

### Comments
- `GET /api/tasks/comments/` - List comments
- `POST /api/tasks/comments/` - Add comment
- `GET /api/tasks/comments/{id}/` - Comment details
- `PUT/PATCH /api/tasks/comments/{id}/` - Update comment
- `DELETE /api/tasks/comments/{id}/` - Delete comment

## Query Examples

- `/api/tasks/?status=todo`
- `/api/tasks/?priority=high`
- `/api/tasks/?due_date=2026-04-22`
- `/api/tasks/?search=resume`
- `/api/tasks/?ordering=due_date`

## Local Setup

```bash
git clone https://github.com/Sridharon5/Task-Management-System.git
cd Task-Management-System
python -m venv .venv
```

Windows:
```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run migrations:
```bash
python manage.py migrate
```

Create admin:
```bash
python manage.py createsuperuser
```

Run server:
```bash
python manage.py runserver
```

## Demo Flows

### 1) Demo Admin (UI + Admin)
1. Open `/`
2. Click **Open Admin as Demo Admin**
3. Auto-login + redirect to `/admin/`
4. On admin logout, user is redirected back to `/`

### 2) Demo User (JWT API)
1. Open `/`
2. Click **Login as Demo User (JWT)**
3. Access and refresh tokens are shown
4. Use access token in `Authorization: Bearer <token>` for task APIs

## Reminder Command

Send reminders for due/overdue tasks:

```bash
python manage.py send_due_task_reminders
```

## Deployment Notes (Vercel)

- Uses `vercel.json` with Django WSGI route
- Static files are handled with WhiteNoise + `collectstatic`
- PostgreSQL is configured via database URL
- Ensure migrations are applied before testing demo flows

## Security Note

Current repo contains a hardcoded database URL (for rapid submission/demo use).
For production, move secrets to environment variables and rotate exposed credentials.

## Author

- **Sridhar Varma**
- GitHub: [Sridharon5](https://github.com/Sridharon5)
