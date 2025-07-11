from django.db import models
from django.utils.translation import gettext_lazy as _


# Status choices for the lifecycle of a scheduled job
class JobStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')  # Waiting to be scheduled or executed
    SCHEDULED = 'scheduled', _('Scheduled')  # Scheduled for execution
    RUNNING = 'running', _('Running')  # Currently being executed
    SUCCESS = 'success', _('Success')  # Executed successfully
    FAILED = 'failed', _('Failed')  # Execution failed


# Main model for a scheduled task/job
class ScheduledJob(models.Model):
    # Human-readable name of the job
    name = models.CharField(
        max_length=255,
    )

    # Fully-qualified import path to the Celery task function
    task_path = models.CharField(
        max_length=255,
        help_text="Import path of the Celery task (e.g., scheduler.tasks.send_email_task)"
    )

    # Positional arguments for the task
    args = models.JSONField(
        blank=True,
        null=True,
        help_text="List of positional args for the task",
    )

    # Keyword arguments for the task
    kwargs = models.JSONField(
        blank=True,
        null=True,
        help_text="Dict of keyword args for the task",
    )

    # Optional one-time execution time (UTC)
    one_off_run_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="If set, task will run once at this datetime (UTC)",
    )

    # Optional cron expression for recurring tasks (e.g. '*/5 * * * *')
    cron_expression = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional: If set, task will run periodically",
    )

    # Current status of the job
    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.PENDING,
        db_index=True,  # Index for filtering by status
    )

    # When the job was last run
    last_run_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    # When the job is scheduled to run next
    next_run_at = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,  # Important for scheduling logic
    )

    # Whether the job is currently active
    is_active = models.BooleanField(
        default=True,
        db_index=True  # Often filtered in scheduler logic
    )

    # Timestamps for job creation and last update
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['one_off_run_time']),
            models.Index(fields=['cron_expression']),
        ]

    def __str__(self):
        return self.name
