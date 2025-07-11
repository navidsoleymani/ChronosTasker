from django.core.management.base import BaseCommand
from scheduler.models import ScheduledJob
from scheduler.services import job_service
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Re-schedule all active jobs into the scheduler engine."

    def handle(self, *args, **options):
        """
        Iterate over all active jobs and re-register them into the scheduler engine.
        Useful after server restart or deployment.
        """
        self.stdout.write(self.style.NOTICE("Refreshing scheduled jobs..."))

        jobs = ScheduledJob.objects.filter(is_active=True)
        scheduled_count = 0

        for job in jobs:
            try:
                job_service.refresh_job(job)
                scheduled_count += 1
                logger.info(f"[SchedulerCommand] Job {job.id} re-scheduled.")
            except Exception as e:
                logger.error(f"[SchedulerCommand] Failed to schedule job {job.id}: {e}")
                self.stderr.write(self.style.ERROR(f"Failed to schedule job {job.id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"{scheduled_count} job(s) scheduled successfully."))
