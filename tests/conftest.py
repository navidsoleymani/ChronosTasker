import os
import django
import pytest
from config.celery import app as celery_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


@pytest.fixture
def celery_app():
    return celery_app
