# reproducer.py
import os
import sys

# Ensure the script's directory is in sys.path
sys.path.append(os.path.dirname(__file__))

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    """
    Simulates the application startup and reproduces the issue with autoreloader and exception raising.
    """
    # Dynamically prepare a minimal Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temporary_settings')
    
    from django.conf import settings
    settings.configure(
        SECRET_KEY='dummy',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'testapp',  # This will be our app to test
        ],
    )
    
    # Attempt to trigger Django startup to reproduce the issue
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'check'])
    
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, AssertionError), "The issue was not reproduced"
        # Exit code 0 when the issue is fixed, meaning the assertion did not raise
        sys.exit(0)

# Definition of the custom app and exception handling follows
class MyException(Exception):
    def __init__(self, value: str, other_thing: str):
        super().__init__(value)
        self.ot = other_thing

from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = "testapp"
    verbose_name = "My App"

    def ready(self):
        raise MyException("foo", "bar")

if __name__ == '__main__':
    # The Django setup process requires certain settings and configurations to be established before models and certain systems can be imported and used. 
    # That's why the actual simulation logic is placed inside a function which is only called when the script is executed directly.
    # This helps to avoid premature initialization errors.
    
    try:
        # Mimic running a Django command to force the AppConfig.ready() method to execute
        main()
    except Exception as unexpected_error: 
        # Catch any unexpected error to avoid confusing outputs
        print_stacktrace(unexpected_error)
        # Exit with a specific code in case of errors not related to the AssertionError
        sys.exit(2)
