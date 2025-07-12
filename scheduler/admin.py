from django.contrib import admin
from scheduler.models import ScheduledJob


@admin.register(ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScheduledJob model.
    Allows viewing and managing scheduled tasks from the Django admin panel.
    """
    list_display = ('id', 'name', 'task_path', 'status', 'is_active', 'next_run_at', 'last_run_at')
    list_filter = ('status', 'is_active', 'cron_expression')
    search_fields = ('name', 'task_path', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_run_at', 'next_run_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'task_path', 'args', 'kwargs')
        }),
        ('Schedule', {
            'fields': ('one_off_run_time', 'cron_expression', 'end_time', 'max_retries')
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'last_run_at', 'next_run_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )