from .base import *

# Enable/disable debug mode
DEBUG = False

# Hosts allowed to access the app
ALLOWED_HOSTS = ['domain.com']

# Database configurations
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'prod_db'),
        'USER': os.getenv('DB_USER', 'prod_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'prod_pass'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Disable Browsable API in production
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]


CORS_ALLOW_ALL_ORIGINS = False
