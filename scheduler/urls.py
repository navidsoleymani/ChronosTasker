from django.urls import path, include
from rest_framework.routers import DefaultRouter

from scheduler.views import ScheduledJobViewSet

# Initialize DRF router to automatically generate routes for the ViewSet
router = DefaultRouter()
router.register(r'jobs', ScheduledJobViewSet, basename='scheduledjob')

urlpatterns = [
    # Include all generated routes for scheduled job management
    path('', include(router.urls)),
]
