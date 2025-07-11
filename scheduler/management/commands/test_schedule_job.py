from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from scheduler.models import ScheduledJob


class Command(BaseCommand):
    help = "Test job scheduling using django-celery-beat backend."

    def handle(self, *args, **options):
        from core.utils.scheduler.scheduler_engine import scheduler_engine

        # Create a one-off job to run in 2 minutes
        job = ScheduledJob.objects.create(
            name="Test One-Off Job",
            task_path="scheduler.tasks.sample_task",
            one_off_run_time=timezone.now() + timedelta(minutes=2),
            is_active=True,
        )

        scheduler_engine.schedule_one_off(job)
        self.stdout.write(self.style.SUCCESS(f"One-off job {job.id} scheduled."))

        # Create a cron job to run every minute
        cron_job = ScheduledJob.objects.create(
            name="Test Cron Job",
            task_path="scheduler.tasks.sample_task",
            cron_expression="*/1 * * * *",
            is_active=True,
        )

        scheduler_engine.schedule_cron(cron_job)
        self.stdout.write(self.style.SUCCESS(f"Cron job {cron_job.id} scheduled."))
