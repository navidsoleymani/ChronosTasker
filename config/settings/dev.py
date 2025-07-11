from .base import *

# Enable/disable debug mode
DEBUG = True

# Hosts allowed to access the app
ALLOWED_HOSTS = ['*']

# Internal IPs for debug toolbar and similar tools
INTERNAL_IPS = ['127.0.0.1']

# Database configurations
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Enable Browsable API
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]

CORS_ALLOW_ALL_ORIGINS = True
