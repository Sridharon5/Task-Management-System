from rest_framework import serializers
from .models import Task, TaskComment


class TaskCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TaskComment
        fields = ["id", "task", "user", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    is_overdue = serializers.ReadOnlyField()
    comments = TaskCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "attachment",
            "is_overdue",
            "reminder_sent",
            "created_at",
            "updated_at",
            "comments",
        ]
        read_only_fields = ["id", "user", "is_overdue", "reminder_sent", "created_at", "updated_at", "comments"]

    def update(self, instance, validated_data):
        # If due_date/status changes, allow sending reminder again if needed
        old_due_date = instance.due_date
        old_status = instance.status
        instance = super().update(instance, validated_data)
        if instance.due_date != old_due_date or instance.status != old_status:
            instance.reminder_sent = False
            instance.save(update_fields=["reminder_sent"])
        return instance