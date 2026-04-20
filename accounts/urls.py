from django.urls import path
from .views import RegisterView, LogoutView, DemoAdminPanelLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("demo-admin/", DemoAdminPanelLoginView.as_view(), name="demo-admin"),
]