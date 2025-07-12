import os

# Retrieve the current Django environment from environment variables.
# Defaults to 'dev' if not explicitly set.
ENV = os.getenv('DJANGO_ENV', 'dev').lower()

# Dynamically import settings based on the current environment.
if ENV == 'prod':
    # Production environment settings
    from .prod import *
elif ENV == 'test':
    # Testing environment settings
    from .test import *
else:
    # Development environment settings (default)
    from .dev import *
