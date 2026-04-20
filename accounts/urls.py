from django.urls import path
from .views import RegisterView, LogoutView, DemoLoginView, DemoAdminPanelLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("demo-login/", DemoLoginView.as_view(), name="demo-login"),
    path("demo-admin/", DemoAdminPanelLoginView.as_view(), name="demo-admin"),
]