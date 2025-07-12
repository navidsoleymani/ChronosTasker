from .base import *

# Enable/disable debug mode
DEBUG = False

# Hosts allowed to access the app
# ALLOWED_HOSTS = ['domain.com']
ALLOWED_HOSTS = ['*']

# Database configurations
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'postgres'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# Disable Browsable API in production
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

CORS_ALLOW_ALL_ORIGINS = False

REDIS_LOCATION = os.getenv('REDIS_LOCATION', 'redis://redis:6379/1')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'TIMEOUT': None,
    }
}

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/1')
