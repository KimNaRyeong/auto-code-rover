# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.db.models.functions import ExtractYear
from django.core.exceptions import FieldError

# Define a temporary directory for SQLite database to address the configuration error
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Minimal Django configuration with database name specified to avoid ImproperlyConfigured error
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()


class MyModel(models.Model):
    duration = models.DurationField()


def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        # Create a new table for testing
        execute_from_command_line(['manage.py', 'makemigrations', '__main__'])
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Insert mock data
        MyModel.objects.create(duration="1 day")

        # Attempt the problematic query and check for ValueError instead of FieldError due to the described issue premise
        results = MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
        assert results.exists(), "No error raised, issue may be fixed"
    except FieldError as e:
        # Expected behavior based on the issue description
        print_stacktrace(e)
        os._exit(0)  # Exit with code 0 indicating the issue was successfully reproduced
    except Exception as e:
        # Handle unexpected errors
        print_stacktrace(e)
        raise AssertionError("Unexpected error encountered")

if __name__ == '__main__':
    reproduce_issue()
