from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, TaskComment
from .serializers import TaskSerializer, TaskCommentSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    filterset_fields = ["status", "priority", "due_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at"]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskComment.objects.filter(task__user=self.request.user)

    def create(self, request, *args, **kwargs):
        task_id = request.data.get("task")
        if not task_id:
            return Response({"detail": "task field is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            task = Task.objects.get(id=task_id, user=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        next_day = today + timedelta(days=1)

        tasks = Task.objects.filter(user=request.user)
        data = {
            "total": tasks.count(),
            "completed": tasks.filter(status=Task.STATUS_DONE).count(),
            "overdue": tasks.filter(due_date__lt=today).exclude(status=Task.STATUS_DONE).count(),
            "due_today": tasks.filter(due_date=today).exclude(status=Task.STATUS_DONE).count(),
            "due_tomorrow": tasks.filter(due_date=next_day).exclude(status=Task.STATUS_DONE).count(),
            "by_status": tasks.values("status").annotate(count=Count("id")),
            "high_priority_open": tasks.filter(priority=Task.PRIORITY_HIGH).exclude(status=Task.STATUS_DONE).count(),
        }
        return Response(data)