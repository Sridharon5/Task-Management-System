from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from tasks.models import Task


class Command(BaseCommand):
    help = "Send reminder emails for tasks due tomorrow or overdue."

    def handle(self, *args, **options):
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        due_tasks = Task.objects.filter(
            reminder_sent=False,
            status__in=[Task.STATUS_TODO, Task.STATUS_IN_PROGRESS],
            due_date__lte=tomorrow,
            user__email__isnull=False,
        ).exclude(user__email="")

        sent_count = 0

        for task in due_tasks:
            if task.due_date < today:
                timing_text = "is overdue"
            elif task.due_date == today:
                timing_text = "is due today"
            else:
                timing_text = "is due tomorrow"

            subject = f"Task Reminder: {task.title}"
            message = (
                f"Hello {task.user.username},\n\n"
                f"Your task '{task.title}' {timing_text}.\n"
                f"Due date: {task.due_date}\n"
                f"Priority: {task.priority}\n"
                f"Status: {task.status}\n\n"
                "Please update or complete the task.\n"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[task.user.email],
                fail_silently=False,
            )

            task.reminder_sent = True
            task.save(update_fields=["reminder_sent"])
            sent_count += 1

        self.stdout.write(self.style.SUCCESS(f"Reminder emails sent: {sent_count}"))
