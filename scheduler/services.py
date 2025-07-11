from django.utils import timezone

from scheduler.models import ScheduledJob, JobStatus


class JobService:
    """
    Service class responsible for job lifecycle operations including
    registration, activation, deactivation, and runtime updates.
    """

    def refresh_job(self, job: ScheduledJob):
        """
        Refresh (re-schedule) a job in the scheduler engine.
        If it's a one-off job in the future or a cron-based job and active, schedule it.
        """

        from core.utils.scheduler import scheduler_engine  # Our scheduler interface

        if not job.is_active:
            return

        # Unschedule any existing instance of this job to avoid duplication
        self.unschedule_job(job)

        # Decide whether it's a one-off or cron-based job
        if job.one_off_run_time and job.one_off_run_time > timezone.now():
            scheduler_engine.schedule_one_off(job)
        elif job.cron_expression:
            scheduler_engine.schedule_cron(job)

    def unschedule_job(self, job: ScheduledJob):
        """
        Remove the job from the scheduler engine (if exists).
        """

        from core.utils.scheduler import scheduler_engine  # Our scheduler interface

        scheduler_engine.remove_job(job.id)

    def handle_job_success(self, job: ScheduledJob):
        """
        Callback to be called after a job has successfully run.
        Updates job metadata.
        """
        job.last_run_at = timezone.now()
        job.status = JobStatus.SUCCESS
        job.save(update_fields=['last_run_at', 'status', 'updated_at'])

    def handle_job_failure(self, job: ScheduledJob):
        """
        Callback to be called if a job execution fails.
        """
        job.status = JobStatus.FAILED
        job.save(update_fields=['status', 'updated_at'])

    def update_next_run_time(self, job: ScheduledJob, next_time):
        """
        Update the next run time (used by the scheduler for cron jobs).
        """
        job.next_run_at = next_time
        job.save(update_fields=['next_run_at', 'updated_at'])


# Singleton instance used throughout the app
job_service = JobService()
