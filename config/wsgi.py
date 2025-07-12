import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'wsgi' application.
# This environment variable tells Django which settings to use.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Get the WSGI application object for serving the Django project.
# This is used by WSGI-compatible web servers (e.g., Gunicorn, uWSGI).
application = get_wsgi_application()
