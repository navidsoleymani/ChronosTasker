from celery import shared_task
from scheduler.models import ScheduledJob


@shared_task(bind=True, name='run_scheduled_job')
def run_scheduled_job(self, job_id):
    """
    Celery task that executes a scheduled job.
    This is the main entry point for both one-off and recurring jobs.
    """
    from scheduler.services import job_service

    try:
        job = ScheduledJob.objects.get(id=job_id)
    except ScheduledJob.DoesNotExist:
        print(f"[Task] Job with id {job_id} does not exist.")
        return

    # Skip execution if job is inactive
    if not job.is_active:
        print(f"[Task] Skipping inactive job {job_id}.")
        return

    print(f"[Task] Running job {job_id}...")

    try:
        # Simulate job execution — this can be replaced by actual logic
        _execute_job_logic(job)

        # Update job status and run time
        job_service.handle_job_success(job)

    except Exception as exc:
        # Handle failure
        print(f"[Task] Job {job_id} failed: {exc}")
        job_service.handle_job_failure(job)
        raise self.retry(exc=exc, countdown=60, max_retries=3)


def _execute_job_logic(job: ScheduledJob):
    """
    Placeholder for actual job logic.
    This should be replaced by the real business logic associated with the job.
    """
    # For demonstration, we're just printing job metadata
    print(f"[Execution] Job {job.id} is executing with payload: {job.payload}")


@shared_task
def sample_task():
    print("This is a scheduled task running...")


@shared_task
def add(x, y):
    """
    A simple task that adds two numbers.
    """
    return x + y
