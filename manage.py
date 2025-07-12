import os
import sys


def main():
    """
    Entry point for Django's command-line utility.

    This function sets the default settings module and then delegates
    execution to Django's management command handler.
    """
    # Set the default Django settings module if not already defined
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        # Import Django's command-line execution utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise a descriptive error if Django is not installed or the environment is misconfigured
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the command-line arguments passed to the script
    execute_from_command_line(sys.argv)


# Run the main function if this script is executed directly
if __name__ == '__main__':
    main()
