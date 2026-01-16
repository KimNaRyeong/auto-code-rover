```python
# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.db.models.functions import ExtractYear
from django.core.exceptions import FieldError

# Minimal Django configuration
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
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
        
        MyModel.objects.create(duration="1 year")
        # Attempt the problematic query
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
        raise AssertionError("The issue is supposed to raise a FieldError")
    except FieldError as e:
        # Expected behavior for this issue
        print_stacktrace(e)
        os._exit(0)  # Exit with code 0 indicating the issue was successfully reproduced
    except Exception as e:
        # Handle unexpected errors
        print_stacktrace(e)
        raise


if __name__ == '__main__':
    reproduce_issue()
```

This script sets up a minimal Django environment, defines a model with a `DurationField`, and attempts to run a query that would trigger the issue described. It is important to note that depending on the Django version and the database backend, the exact exception and behavior might vary.

Also, note the use of `os._exit(0)` to ensure a clean exit with status code 0 in case the error is successfully reproduced, bypassing Django's usual system checks and command line management setup which might otherwise interfere with or mask the specific `FieldError` we are interested in catching and demonstrating.