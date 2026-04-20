# Task Management System (Django + DRF)

Task Manager backend project built with Django and Django REST Framework, deployed on Vercel.
The project now uses a clean **Admin-only demo flow**: one click logs into Demo Admin and opens Django Admin.

## Live Demo

- App URL: `https://task-management-system-izdeb35vg-maloth-sridhar-varmas-projects.vercel.app/`
- Admin demo login: `GET /api/auth/demo-admin/`

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

## Demo Flow

### Demo Admin (UI + Admin)
1. Open `/`
2. Click **Login as Demo Admin**
3. Auto-login + redirect to `/admin/`
4. On admin logout, user is redirected back to `/`

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
