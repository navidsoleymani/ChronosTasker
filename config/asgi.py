import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' application.
# This environment variable specifies which settings to load.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Get the ASGI application callable to serve the Django project.
# Required for asynchronous servers (e.g., Daphne, Uvicorn, Hypercorn).
application = get_asgi_application()
