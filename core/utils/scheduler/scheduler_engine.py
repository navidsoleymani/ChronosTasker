import logging
from celery import current_app
from celery.schedules import crontab
from django.utils import timezone
from scheduler.models import ScheduledJob
from scheduler.tasks import run_scheduled_job

logger = logging.getLogger(__name__)


class SchedulerEngine:
    """
    SchedulerEngine handles dynamic scheduling of jobs using Celery's `apply_async`
    for one-off tasks and `add_periodic_task` for cron-style recurring tasks.

    NOTE: Dynamic periodic tasks using Celery Beat do not persist across restarts
    unless you're using `django-celery-beat`.
    """

    def schedule_one_off(self, job: ScheduledJob):
        """
        Schedule a one-time task using Celery's `apply_async`.

        Args:
            job (ScheduledJob): Job instance to be scheduled.
        """
        eta = job.one_off_run_time

        if eta and eta > timezone.now():
            run_scheduled_job.apply_async(args=[job.id], eta=eta)
            logger.info(f"[SchedulerEngine] One-off job {job.id} scheduled at {eta}.")
        else:
            logger.warning(f"[SchedulerEngine] Invalid or past datetime for job {job.id}: {eta}")

    def schedule_cron(self, job: ScheduledJob):
        """
        Schedule a recurring job using a cron expression via Celery's `add_periodic_task`.

        WARNING:
        - This approach does NOT persist across process restarts.
        - For production-grade usage, consider `django-celery-beat`.

        Args:
            job (ScheduledJob): Job instance with a valid cron expression.
        """
        try:
            # Parse cron expression like "*/5 * * * *"
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

            logger.info(f"[SchedulerEngine] Cron job {job.id} scheduled with expression '{job.cron_expression}'.")

        except ValueError as ve:
            logger.error(f"[SchedulerEngine] Malformed cron expression for job {job.id}: {job.cron_expression}. Error: {ve}")
        except Exception as e:
            logger.error(f"[SchedulerEngine] Failed to schedule cron job {job.id}: {e}")

    def remove_job(self, job_id: int):
        """
        Attempt to remove a job from the scheduler. No-op for now.

        NOTE:
        Celery does not support dynamic removal of periodic tasks at runtime.
        Use `django-celery-beat` to support persistent removal.
        """
        logger.warning(f"[SchedulerEngine] Removal of job {job_id} is not supported in this setup.")


# Singleton instance used throughout the project
scheduler_engine = SchedulerEngine()
