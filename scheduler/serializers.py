from rest_framework import serializers

from scheduler.models import ScheduledJob


class ScheduledJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledJob
        fields = [
            'id', 'name', 'task_path', 'args', 'kwargs',
            'one_off_run_time', 'cron_expression',
            'status', 'last_run_at', 'next_run_at',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'status', 'last_run_at', 'next_run_at', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Custom validation to ensure the user either sets a one-off run time or a cron expression, but not both.
        """
        one_off = data.get('one_off_run_time')
        cron = data.get('cron_expression')

        if not one_off and not cron:
            raise serializers.ValidationError("You must provide either 'one_off_run_time' or 'cron_expression'.")
        if one_off and cron:
            raise serializers.ValidationError("You cannot provide both 'one_off_run_time' and 'cron_expression'.")

        return data
