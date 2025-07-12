from django.urls import path, include

# Define the app namespace for versioning the API
app_name = 'v1'

# URL patterns for version 1 of the API
urlpatterns = [
    # Include all scheduler-related routes under the /scheduler/ path
    path('scheduler/', include('scheduler.urls')),
]
