from django.urls import path, include

app_name = 'v1'
urlpatterns = [
    path('scheduler', include('scheduler.urls')),
]
