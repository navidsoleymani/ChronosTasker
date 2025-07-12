import logging
import traceback
from importlib import import_module

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
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
    """
    from scheduler.services import job_service

    try:
        job = ScheduledJob.objects.get(id=job_id)
    except ScheduledJob.DoesNotExist:
        logger.warning(f"[Task] Job with id {job_id} does not exist.")
        return

    # Check if the job is active and not expired
    if not job.is_active:
        logger.info(f"[Task] Skipping inactive job {job_id}.")
        return

    if job.end_time and timezone.now() > job.end_time:
        logger.info(f"[Task] Skipping expired job {job_id} (past end_time).")
        return

    logger.info(f"[Task] Running job {job_id} ({job.name}) at {timezone.now()}")

    # Update job as running
    job.status = JobStatus.RUNNING
    job.last_run_at = timezone.now()
    job.save(update_fields=['status', 'last_run_at'])

    try:
        # Dynamically import and execute the task function
        result = _execute_job_logic(job)

        # Handle success
        job.result = str(result)[:2048]  # truncate if large
        job_service.handle_job_success(job, result=result)
        job.save(update_fields=['result', 'status', 'last_run_at', 'updated_at'])
        logger.info(f"[Task] Job {job_id} executed successfully.")
        return result

    except Exception as exc:
        # Handle failure
        error_msg = f"[Task] Job {job_id} failed: {exc}\n{traceback.format_exc()}"
        logger.error(error_msg)
        job.error_message = str(exc)[:2048]  # truncate if large
        job_service.handle_job_failure(job, error_message=str(exc))
        job.save(update_fields=['error_message', 'status', 'updated_at'])

        # Retry with job-defined max_retries
        if job.max_retries > 0:
            try:
                rkw = {
                    'exc': exc,
                    'countdown': 60,
                    'max_retries': job.max_retries,
                }
                if job.end_time:
                    rkw['expires'] = job.end_time
                raise self.retry(**rkw)
            except MaxRetriesExceededError:
                logger.warning(f"[Task] Max retries exceeded for job {job_id}.")
                return
            except Exception as retry_error:
                logger.error(f"[Task] Retry failed to queue for job {job_id}: {retry_error}")
                return


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


@shared_task(bind=True, name='scheduler.tasks.send_email_task')
def send_email_task(self, recipient_email, subject="No Subject", body=""):
    """
    A mocked task that simulates sending an email.

    Args:
        recipient_email (str): The recipient's email address.
        subject (str): Subject line of the email.
        body (str): Content of the email body.

    Returns:
        str: Success message for the simulated email.
    """
    logger.info(f"[EmailTask] Sending email to {recipient_email}")
    logger.info(f"[EmailTask] Subject: {subject}")
    logger.info(f"[EmailTask] Body: {body}")

    # todo Simulate sending delay or logic here
    return f"Email sent to {recipient_email} with subject: {subject}"
