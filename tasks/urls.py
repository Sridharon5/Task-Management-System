from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskCommentViewSet, DashboardView

router = DefaultRouter()
router.register(r"", TaskViewSet, basename="task")
router.register(r"comments", TaskCommentViewSet, basename="task-comment")

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("", include(router.urls)),
]