import os
from pathlib import Path

import dotenv
from django.utils.translation import gettext_lazy as _

# Load environment variables from .env file
dotenv.load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Django secret key
SECRET_KEY = os.getenv('SECRET', 'mY1keY**')

# Installed applications
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'drf_yasg',  # For Swagger/OpenAPI schema generation
    'corsheaders',
    'rest_framework',
    'django_filters',
    'django_celery_beat',  # Enables periodic task management in Django Admin

    # apps
    'scheduler.apps.SchedulerConfig',
]

# Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration module
ROOT_URLCONF = 'config.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path
WSGI_APPLICATION = 'config.wsgi.application'

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization and internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = (
    ('en', _('English')),
    ('fa', _('Farsi')),
)

# Paths for locale translation files
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfilesdirs'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediaroot')

# Default field type for auto primary keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Disable reverting changes in django-simple-history (if used)
SIMPLE_HISTORY_REVERT_DISABLED = True

# Automatically append slash to URLs
APPEND_SLASH = True

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_METHODS = (
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
)
CORS_ALLOW_HEADERS = ('*',)
CORS_ALLOW_CREDENTIALS = True

# Cache settings using Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_LOCATION', 'redis://127.0.0.1:6379'),
        'TIMEOUT': None,
    }
}

# CSRF protection trusted origins
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
]

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/min',  # Requests per minute for unauthenticated users
        'user': '1000/min',  # Requests per minute for authenticated users
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Celery configuration (using Redis as broker and result backend)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
