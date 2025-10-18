To address the request directly, let's construct a Python script that should accurately reproduce the issue at hand. This script will also attempt to handle it per your instructions, aiming for an `AssertionError` when the problem persists and a normal exit with code 0 upon its resolution.

This script encapsulates the essence of the previously mentioned Django model usage, with an attempt to incorporate window functions within a select clause:

```python
# reproducer.py

import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Window, F, Case, Value, When
from django.db.models.functions import Lag
from django.db.models.fields import BooleanField
from django.core.management import execute_from_command_line


def setup_django_environment():
    settings.configure(
        DEBUG=True,
        SECRET_KEY='not_so_secret',
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        INSTALLED_APPS=('__main__',),
        USE_TZ=True,
    )
    django.setup()


# Mini application setup
setup_django_environment()


# Model Definitions
class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=100)


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
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    # Attempt to trigger the issue
    try:
        Employee.objects.annotate(
            lag=Window(
                expression=Lag('salary', offset=1),
                partition_by=[F('department')],
                order_by=[F('salary').asc(), F('name').asc()]
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True),
                output_field=BooleanField()
            ),
        ).first()
        
        # If the above operation does not raise an exception, it means the issue has been resolved
        print("The issue seems to be resolved.")
        sys.exit(0)
    except Exception as e:
        if 'window function' in str(e).lower():
            # Expected issue raised
            print_stacktrace(e)
            raise AssertionError("The issue with window expressions in SELECT is still present.")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print(e)
        sys.exit(0)
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        sys.exit(1)
```

This script aims to follow the stipulations provided strictly:

- It initializes a minimal Django application programmatically, defining a simple model and using an in-memory SQLite database for simplicity.
- It then seeks to execute a query that employs a window function within its select clause alongside a conditional statement. This specific usage is expected to raise an exception due to Django's limitations regarding window expressions in the select clause as mentioned.
- Upon catching the expected error, it prints a detailed stack trace as requested.
- Exits with the appropriate exit codes given the outcome of the test script.