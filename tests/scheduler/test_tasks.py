from datetime import timedelta

import pytest
from django.utils import timezone

from scheduler.models import ScheduledJob, JobStatus
from scheduler.tasks import add
from scheduler.tasks import run_scheduled_job


@pytest.mark.celery(result_backend='rpc://')
def test_add_task():
    """
    Test the add task returns the correct result.
    """
    result = add.delay(4, 6)
    # Wait for the task to finish and get the result
    assert result.get(timeout=10) == 10


@pytest.mark.django_db
def test_run_send_email_task_via_scheduled_job(caplog):
    """
    Integration test to validate successful execution of a ScheduledJob
    that targets the `send_email_task` defined in `scheduler.tasks`.

    This test ensures:
    - Dynamic task resolution via `task_path`
    - Correct task execution with positional and keyword arguments
    - Job status is updated appropriately
    - Logs and result are persisted correctly
    """

    # Create a ScheduledJob targeting the send_email_task
    job = ScheduledJob.objects.create(
        name="Test Email Job",
        task_path="scheduler.tasks.send_email_task",
        args=["test@example.com"],
        kwargs={"subject": "Hello", "body": "This is a test."},
        is_active=True,
        one_off_run_time=timezone.now() + timedelta(seconds=1),
    )

    # Execute the job using the main runner task
    result = run_scheduled_job.apply(args=(job.id,))

    # Validate task ran successfully
    assert result.successful(), "Celery task did not execute successfully"

    # Validate expected output from send_email_task
    expected_output = (
        "Sending email to test@example.com\n"
        "Subject: Hello\n"
        "Body: This is a test."
    )
    assert expected_output in result.result

    # Validate job database state updates
    job.refresh_from_db()
    assert job.status == JobStatus.SUCCESS
    assert job.result and expected_output in job.result
    assert job.last_run_at is not None

    # Validate log output
    assert any(
        "executed successfully" in record.message.lower()
        for record in caplog.records
    ), "Expected success log not found"
