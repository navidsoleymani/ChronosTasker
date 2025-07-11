from .base import *

# Enable debugging during tests
DEBUG = True

# Use in-memory SQLite database for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use dummy cache backend to avoid external dependencies like Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Simplify password hashing to speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Celery configuration for testing - tasks run locally and synchronously
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# Reduce DRF throttling in tests to avoid rate limit issues
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100000/min',
    'user': '100000/min',
}
