from django.urls import path
from .views import RegisterView, LogoutView, DemoLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("demo-login/", DemoLoginView.as_view(), name="demo-login"),
]