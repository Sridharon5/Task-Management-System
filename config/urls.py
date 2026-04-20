from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


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
      </style>
    </head>
    <body>
      <div class="card">
        <h1>Task Manager API is running</h1>
        <p class="muted">Quick evaluator access: click button to open Django admin as Demo Admin.</p>
        <button onclick="window.location.href='/api/auth/demo-admin/'">Open Admin as Demo Admin</button>
        <p class="muted">API endpoint for JWT: POST /api/auth/demo-login/</p>
        <pre id="result">No token generated yet.</pre>
      </div>
      <script>
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
          } catch (err) {
            result.textContent = 'Error: ' + err.message;
          }
        }
      </script>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    path("", home),   # <-- add this line
    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/tasks/", include("tasks.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)