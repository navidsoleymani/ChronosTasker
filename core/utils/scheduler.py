from celery import current_app
from django.utils import timezone

from scheduler.models import ScheduledJob


class SchedulerEngine:
    """
    SchedulerEngine acts as a central interface to add, update,
    or remove scheduled jobs using Celery's scheduling capabilities.
    """

    def schedule_one_off(self, job: ScheduledJob):
        """
        Schedule a one-off task to be executed at a specific datetime using Celery's `apply_async`.
        """
        from scheduler.tasks import run_scheduled_job

        eta = job.one_off_run_time

        if eta and eta > timezone.now():
            run_scheduled_job.apply_async(args=[job.id], eta=eta)
            print(f"[Scheduler] One-off job {job.id} scheduled at {eta}.")

    def schedule_cron(self, job: ScheduledJob):
        """
        Schedule a recurring job using Celery Beat and periodic task registration.

        Note:
        - This method assumes dynamic periodic task creation.
        - In production, it's better to store these definitions in a DB (like `django-celery-beat`)
        """
        from scheduler.tasks import run_scheduled_job

        # Convert cron_expression to schedule kwargs (e.g. minute="*", hour="*", etc.)
        try:
            from celery.schedules import crontab

            # Naively parse cron string: "*/5 * * * *"
            minute, hour, day_of_month, month, day_of_week = job.cron_expression.split()
            schedule = crontab(
                minute=minute,
                hour=hour,
                day_of_month=day_of_month,
                month_of_year=month,
                day_of_week=day_of_week,
            )

            task_name = f"scheduler.job.{job.id}"

            current_app.add_periodic_task(
                schedule,
                run_scheduled_job.s(job.id),
                name=task_name,
                options={'queue': 'default'}
            )

            print(f"[Scheduler] Cron job {job.id} registered with schedule {job.cron_expression}")
        except Exception as e:
            print(f"[Scheduler] Failed to schedule cron job {job.id}: {e}")

    def remove_job(self, job_id: int):
        """
        Remove job from scheduler if supported.
        This is a placeholder. Celery's periodic task removal is non-trivial.
        """
        # With default Celery, there's no direct way to remove tasks dynamically at runtime.
        # If using `django-celery-beat`, you can delete the entry from PeriodicTask model.
        print(f"[Scheduler] Requested removal of job {job_id} — not supported in this mode.")


# Export singleton instance
scheduler_engine = SchedulerEngine()
