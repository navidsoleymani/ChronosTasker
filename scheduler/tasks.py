import logging
import traceback
from importlib import import_module

from celery import shared_task
from django.utils import timezone
from scheduler.models import ScheduledJob, JobStatus

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='run_scheduled_job')
def run_scheduled_job(self, job_id):
    """
    Celery task that executes a scheduled job.
    This task serves as the main entry point for running both one-off and recurring jobs.

    Args:
        job_id (int): ID of the ScheduledJob instance to run.
        :param self: ...
    """
    from scheduler.services import job_service

    try:
        job = ScheduledJob.objects.get(id=job_id)
    except ScheduledJob.DoesNotExist:
        logger.warning(f"[Task] Job with id {job_id} does not exist.")
        return

    if not job.is_active:
        logger.info(f"[Task] Skipping inactive job {job_id}.")
        return

    logger.info(f"[Task] Running job {job_id} ({job.name})")

    # Update job as running
    job.status = JobStatus.RUNNING
    job.last_run_at = timezone.now()
    job.save(update_fields=['status', 'last_run_at'])

    try:
        # Dynamically import and execute the task function
        result = _execute_job_logic(job)

        # Handle success
        job_service.handle_job_success(job, result=result)
        logger.info(f"[Task] Job {job_id} executed successfully.")
        return result

    except Exception as exc:
        # Handle failure
        error_msg = f"[Task] Job {job_id} failed: {exc}\n{traceback.format_exc()}"
        logger.error(error_msg)
        job_service.handle_job_failure(job, error_message=str(exc))

        # Retry the task with exponential backoff (optional)
        raise self.retry(exc=exc, countdown=60, max_retries=3)


def _execute_job_logic(job: ScheduledJob):
    """
    Dynamically imports and executes the task function specified in the job's `task_path`.

    Args:
        job (ScheduledJob): The job instance to execute.

    Returns:
        Any: The result of the executed task.
    """
    if not job.task_path:
        raise ValueError("Task path is not defined for this job.")

    module_path, func_name = job.task_path.rsplit('.', 1)
    module = import_module(module_path)
    task_func = getattr(module, func_name)

    logger.debug(f"[Execution] Executing job {job.id} with args={job.args} kwargs={job.kwargs}")
    return task_func(*job.args or [], **job.kwargs or {})


@shared_task
def sample_task():
    """
    Sample placeholder task.
    """
    logger.info("[Sample] This is a scheduled sample task running...")


@shared_task
def add(x, y):
    """
    A simple demonstration task that adds two numbers.

    Args:
        x (int | float): First number.
        y (int | float): Second number.

    Returns:
        int | float: The result of addition.
    """
    return x + y
