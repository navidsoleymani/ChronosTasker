import logging
from datetime import datetime

from django.utils import timezone
from croniter import croniter

from scheduler.models import ScheduledJob, JobStatus

logger = logging.getLogger(__name__)


class JobService:
    """
    Service class responsible for job lifecycle operations including
    registration, activation, deactivation, and runtime metadata updates.
    """

    def refresh_job(self, job: ScheduledJob):
        """
        Refresh (re-schedule) a job in the scheduler engine.

        This handles both one-off and recurring cron jobs:
        - One-off jobs must have a future `one_off_run_time`
        - Cron jobs must have a valid `cron_expression`

        Existing job instances are unscheduled before re-adding them.
        """
        from core.utils.scheduler import engine as scheduler_engine

        if not job.is_active:
            logger.info(f"[JobService] Job {job.id} is inactive. Skipping scheduling.")
            return

        self.unschedule_job(job)

        if job.one_off_run_time and job.one_off_run_time > timezone.now():
            scheduler_engine.schedule_one_off(job)
            logger.info(f"[JobService] Scheduled one-off job {job.id} at {job.one_off_run_time}.")
        elif job.cron_expression:
            scheduler_engine.schedule_cron(job)
            logger.info(f"[JobService] Scheduled cron job {job.id} with expression '{job.cron_expression}'.")

            # Compute next_run_at using croniter for metadata tracking
            try:
                base_time = timezone.now()
                next_run = croniter(job.cron_expression, base_time).get_next(datetime)
                job.next_run_at = next_run
                job.save(update_fields=['next_run_at', 'updated_at'])
                logger.debug(f"[JobService] Updated next_run_at for job {job.id} to {next_run}.")
            except Exception as e:
                logger.error(f"[JobService] Failed to calculate next_run_at for job {job.id}: {e}")

    def unschedule_job(self, job: ScheduledJob):
        """
        Remove the job from the scheduler engine (if it exists).
        """
        from core.utils.scheduler import engine as scheduler_engine

        scheduler_engine.remove_job(job.id)
        logger.info(f"[JobService] Unscheduling job {job.id} from scheduler.")

    def handle_job_success(self, job: ScheduledJob):
        """
        Callback to be called after a job has successfully run.
        Updates run time and status.
        """
        job.last_run_at = timezone.now()
        job.status = JobStatus.SUCCESS
        job.save(update_fields=['last_run_at', 'status', 'updated_at'])
        logger.info(f"[JobService] Job {job.id} executed successfully.")

    def handle_job_failure(self, job: ScheduledJob):
        """
        Callback to be called if a job execution fails.
        Updates job status accordingly.
        """
        job.status = JobStatus.FAILED
        job.save(update_fields=['status', 'updated_at'])
        logger.warning(f"[JobService] Job {job.id} execution failed.")

    def update_next_run_time(self, job: ScheduledJob, next_time: datetime):
        """
        Update the next scheduled run time for the job.
        Usually invoked by the scheduler engine for cron jobs.
        """
        job.next_run_at = next_time
        job.save(update_fields=['next_run_at', 'updated_at'])
        logger.debug(f"[JobService] Manually updated next_run_at for job {job.id} to {next_time}.")


# Singleton instance used across the application
job_service = JobService()
