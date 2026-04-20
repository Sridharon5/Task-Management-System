from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import logout as django_logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def admin_logout_redirect(request):
    django_logout(request)
    return redirect("/")


def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Task Manager API</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 40px; background:#f7f7fb; color:#222; }
        .card { max-width: 760px; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,.06);}
        h1 { margin-top: 0; }
        button { background:#0d6efd; color:#fff; border:none; border-radius:8px; padding:10px 16px; cursor:pointer; font-weight:600; }
        button:hover { background:#0b5ed7; }
        pre { background:#0f172a; color:#e2e8f0; padding:12px; border-radius:8px; overflow:auto; }
        .muted { color:#666; font-size:14px; }
        .row { display:flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }
        input, textarea, select { width: 100%; padding: 8px; border: 1px solid #d4d4d8; border-radius: 6px; }
        .task-card { border: 1px solid #e4e4e7; border-radius: 8px; padding: 10px; margin-bottom: 8px; background: #fafafa; }
        .hidden { display: none; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>Task Manager API is running</h1>
        <p class="muted">Quick evaluator access: use Demo Admin for Django admin or Demo User for JWT API.</p>
        <div class="row">
          <button onclick="window.location.href='/api/auth/demo-admin/'">Open Admin as Demo Admin</button>
          <button onclick="demoLogin()">Login as Demo User (JWT)</button>
          <button onclick="loadTasks()">Load My Tasks</button>
        </div>
        <div id="demo-app" class="hidden">
          <h3>Demo User Task Workspace</h3>
          <div class="row">
            <button onclick="loadTasks()">Refresh Tasks</button>
          </div>
          <div class="row">
            <div style="flex:1; min-width:220px;">
              <label>Title</label>
              <input id="task-title" placeholder="Ex: Complete resume update" />
            </div>
            <div style="flex:1; min-width:220px;">
              <label>Due Date</label>
              <input id="task-due" type="date" />
            </div>
          </div>
          <div class="row">
            <div style="flex:1; min-width:220px;">
              <label>Status</label>
              <select id="task-status">
                <option value="todo">todo</option>
                <option value="in_progress">in_progress</option>
                <option value="done">done</option>
              </select>
            </div>
            <div style="flex:1; min-width:220px;">
              <label>Priority</label>
              <select id="task-priority">
                <option value="low">low</option>
                <option value="medium" selected>medium</option>
                <option value="high">high</option>
              </select>
            </div>
          </div>
          <div class="row">
            <div style="width:100%;">
              <label>Description</label>
              <textarea id="task-description" rows="3" placeholder="Task description"></textarea>
            </div>
          </div>
          <div class="row">
            <button onclick="createTask()">Add Task</button>
          </div>
          <div id="tasks-list"></div>
        </div>
        <p class="muted">JWT endpoint: POST /api/auth/demo-login/</p>
        <pre id="result">No token generated yet.</pre>
      </div>
      <script>
        function getToken() {
          return localStorage.getItem('demo_access_token');
        }

        function authHeaders() {
          const token = getToken();
          return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
          };
        }

        function renderTasks(tasks) {
          const container = document.getElementById('tasks-list');
          if (!tasks.length) {
            container.innerHTML = '<p class="muted">No tasks found for this user.</p>';
            return;
          }
          container.innerHTML = tasks.map(t => `
            <div class="task-card">
              <strong>${t.title}</strong><br/>
              <span>Status: ${t.status} | Priority: ${t.priority} | Due: ${t.due_date}</span><br/>
              <span>${t.description || ''}</span>
            </div>
          `).join('');
        }

        async function demoLogin() {
          const result = document.getElementById('result');
          result.textContent = 'Logging in...';
          try {
            const resp = await fetch('/api/auth/demo-login/', {
              method: 'POST',
              headers: { 'Accept': 'application/json' }
            });
            const raw = await resp.text();
            let data;
            try {
              data = JSON.parse(raw);
            } catch {
              data = { detail: raw };
            }
            if (!resp.ok) {
              result.textContent = JSON.stringify({
                status: resp.status,
                message: 'Demo login failed',
                response: data
              }, null, 2);
              return;
            }
            localStorage.setItem('demo_access_token', data.access);
            localStorage.setItem('demo_refresh_token', data.refresh);
            result.textContent = JSON.stringify(data, null, 2);
            document.getElementById('demo-app').classList.remove('hidden');
            await loadTasks();
          } catch (err) {
            result.textContent = 'Error: ' + err.message;
          }
        }

        async function loadTasks() {
          const result = document.getElementById('result');
          const token = getToken();
          if (!token) {
            result.textContent = 'Login as Demo User first.';
            return;
          }
          try {
            const resp = await fetch('/api/tasks/', { headers: authHeaders() });
            const raw = await resp.text();
            const data = JSON.parse(raw);
            if (!resp.ok) {
              result.textContent = JSON.stringify(data, null, 2);
              return;
            }
            document.getElementById('demo-app').classList.remove('hidden');
            renderTasks(data);
            result.textContent = 'Tasks loaded successfully.';
          } catch (err) {
            result.textContent = 'Error while loading tasks: ' + err.message;
          }
        }

        async function createTask() {
          const result = document.getElementById('result');
          const token = getToken();
          if (!token) {
            result.textContent = 'Login as Demo User first.';
            return;
          }

          const payload = {
            title: document.getElementById('task-title').value.trim(),
            description: document.getElementById('task-description').value.trim(),
            due_date: document.getElementById('task-due').value,
            status: document.getElementById('task-status').value,
            priority: document.getElementById('task-priority').value
          };

          if (!payload.title || !payload.due_date) {
            result.textContent = 'Title and due date are required.';
            return;
          }

          try {
            const resp = await fetch('/api/tasks/', {
              method: 'POST',
              headers: authHeaders(),
              body: JSON.stringify(payload)
            });
            const raw = await resp.text();
            const data = JSON.parse(raw);
            if (!resp.ok) {
              result.textContent = JSON.stringify(data, null, 2);
              return;
            }
            result.textContent = 'Task created successfully.';
            document.getElementById('task-title').value = '';
            document.getElementById('task-description').value = '';
            await loadTasks();
          } catch (err) {
            result.textContent = 'Error while creating task: ' + err.message;
          }
        }
      </script>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    path("", home),   # <-- add this line
    path("admin/logout/", admin_logout_redirect),
    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/tasks/", include("tasks.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)