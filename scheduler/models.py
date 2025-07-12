from croniter import croniter
from django.core.exceptions import ValidationError
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
        verbose_name=_('Name'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
        help_text="Optional text description for understanding the job purpose."
    )

    # Fully-qualified import path to the Celery task function
    task_path = models.CharField(
        verbose_name=_('Task Path'),
        max_length=255,
        help_text="Import path of the Celery task (e.g., scheduler.tasks.send_email_task)"
    )

    # Positional arguments for the task
    args = models.JSONField(
        verbose_name=_('*args'),
        blank=True,
        null=True,
        help_text="List of positional args for the task",
    )

    # Keyword arguments for the task
    kwargs = models.JSONField(
        verbose_name=_('**kwargs'),
        blank=True,
        null=True,
        help_text="Dict of keyword args for the task",
    )

    # Optional one-time execution time (UTC)
    one_off_run_time = models.DateTimeField(
        verbose_name=_('One Off Run Time'),
        blank=True,
        null=True,
        help_text="If set, task will run once at this datetime (UTC)",
    )

    # Optional cron expression for recurring tasks (e.g. '*/5 * * * *')
    cron_expression = models.CharField(
        verbose_name=_('Cron Expression'),
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional: If set, task will run periodically",
    )
    end_time = models.DateTimeField(
        verbose_name=_('End Time'),
        blank=True,
        null=True,
        help_text="If set, no executions will be scheduled after this datetime (UTC)."
    )
    max_retries = models.PositiveIntegerField(
        verbose_name=_('Max Retries'),
        default=0,
        help_text="Maximum retry attempts if the task execution fails."
    )

    # Current status of the job
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.PENDING,
        db_index=True,  # Index for filtering by status
    )

    # When the job was last run
    last_run_at = models.DateTimeField(
        verbose_name=_('Last Run At'),
        blank=True,
        null=True,
    )

    # When the job is scheduled to run next
    next_run_at = models.DateTimeField(
        verbose_name=_('Next Run At'),
        blank=True,
        null=True,
        db_index=True,  # Important for scheduling logic
    )

    # Whether the job is currently active
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        default=True,
        db_index=True  # Often filtered in scheduler logic
    )

    # Timestamps for job creation and last update
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated At'),
        auto_now=True,
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['one_off_run_time']),
            models.Index(fields=['cron_expression']),
        ]
        verbose_name = _('Scheduled Job')
        verbose_name_plural = _('Scheduled Jobs')

    def clean(self):
        """
        Validate the cron expression if provided.
        """
        if self.cron_expression and not croniter.is_valid(self.cron_expression):
            raise ValidationError("Invalid cron expression.")

        if not self.cron_expression and not self.one_off_run_time:
            raise ValidationError("Either cron_expression or one_off_run_time must be provided.")

    def __str__(self):
        return self.name
