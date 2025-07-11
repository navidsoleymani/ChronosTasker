from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from scheduler.models import ScheduledJob
from scheduler.serializers import ScheduledJobSerializer
from scheduler.services import job_service


class ScheduledJobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing scheduled jobs.
    Supports standard CRUD operations and additional actions
    like activating or deactivating a job.
    """
    queryset = ScheduledJob.objects.all()
    serializer_class = ScheduledJobSerializer

    def perform_create(self, serializer):
        """
        Hook to handle post-creation logic such as scheduling the job.
        """
        job = serializer.save()
        job_service.refresh_job(job)

    def perform_update(self, serializer):
        """
        Hook to handle job rescheduling after update.
        """
        job = serializer.save()
        job_service.refresh_job(job)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """
        Custom action to activate a scheduled job.
        Schedules the job immediately upon activation.
        """
        job = self.get_object()
        if job.is_active:
            return Response({"detail": "Job is already active."}, status=status.HTTP_400_BAD_REQUEST)

        job.is_active = True
        job.save()

        job_service.refresh_job(job)
        return Response({"detail": "Job activated and scheduled successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """
        Custom action to deactivate a scheduled job.
        Disables future execution but does not cancel already scheduled tasks.
        """
        job = self.get_object()
        if not job.is_active:
            return Response({"detail": "Job is already inactive."}, status=status.HTTP_400_BAD_REQUEST)

        job.is_active = False
        job.save()

        return Response({"detail": "Job deactivated."}, status=status.HTTP_200_OK)
