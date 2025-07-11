import logging
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils import timezone
from scheduler.models import ScheduledJob
from scheduler.tasks import run_scheduled_job
import json

logger = logging.getLogger(__name__)


class BeatSchedulerEngine:
    """
    Persistent scheduler using django-celery-beat for cron-based jobs.
    One-off jobs are still scheduled via Celery's apply_async.
    """

    def schedule_one_off(self, job: ScheduledJob):
        """
        Schedule a one-time job using Celery's apply_async.
        """
        eta = job.one_off_run_time

        if eta and eta > timezone.now():
            run_scheduled_job.apply_async(args=[job.id], eta=eta)
            logger.info(f"[BeatScheduler] One-off job {job.id} scheduled at {eta}.")
        else:
            logger.warning(f"[BeatScheduler] Invalid one-off run time for job {job.id}: {eta}")

    def schedule_cron(self, job: ScheduledJob):
        """
        Schedule a recurring job via django-celery-beat.
        This creates a PeriodicTask in DB, which survives process restarts.
        """
        try:
            # Parse cron expression
            minute, hour, day_of_month, month, day_of_week = job.cron_expression.split()

            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_month=day_of_month,
                month_of_year=month,
                day_of_week=day_of_week,
                timezone="UTC",
            )

            task_name = f"scheduler.job.{job.id}"

            PeriodicTask.objects.update_or_create(
                name=task_name,
                defaults={
                    "task": "run_scheduled_job",  # must match registered task name
                    "crontab": schedule,
                    "args": json.dumps([job.id]),
                    "enabled": job.is_active,
                    "start_time": timezone.now(),
                    "expires": job.end_time,
                }
            )

            logger.info(f"[BeatScheduler] Cron job {job.id} registered in DB.")

        except ValueError as ve:
            logger.error(f"[BeatScheduler] Invalid cron format for job {job.id}: {ve}")
        except Exception as e:
            logger.error(f"[BeatScheduler] Failed to schedule job {job.id} in DB: {e}")

    def remove_job(self, job_id: int):
        """
        Remove job from persistent periodic task list.
        """
        task_name = f"scheduler.job.{job_id}"
        deleted, _ = PeriodicTask.objects.filter(name=task_name).delete()

        if deleted:
            logger.info(f"[BeatScheduler] Job {job_id} removed from PeriodicTask.")
        else:
            logger.warning(f"[BeatScheduler] No PeriodicTask found for job {job_id}.")


# Singleton instance
beat_scheduler_engine = BeatSchedulerEngine()
