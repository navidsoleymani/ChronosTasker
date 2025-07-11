import os

# Set default environment
ENV = os.getenv('DJANGO_ENV', 'dev').lower()

if ENV == 'prod':
    from .prod import *
elif ENV == 'test':
    from .test import *
else:
    from .dev import *
