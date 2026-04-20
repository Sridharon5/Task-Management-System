from django.contrib import admin
from .models import Task, TaskComment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "priority", "due_date", "reminder_sent", "created_at")
    list_filter = ("status", "priority", "due_date", "reminder_sent")
    search_fields = ("title", "description", "user__username")


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "user", "created_at")
    search_fields = ("comment", "task__title", "user__username")