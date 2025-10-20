```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Case, Value, When, F, Window, fields
from django.db.models.functions import Lag
from django.core.management import execute_from_command_line

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

# Define settings for Django
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script runs as the "__main__" module.
    ),
    USE_TZ=True,
)

django.setup()

# Define a simple model for demonstration.
class Employee(models.Model):
    name = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=255)

    class Meta:
        app_label = '__main__'

# Reproducing the issue
def run_test():
    try:
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        # Simulate Django's handling of database tables etc.
        execute_from_command_line(['manage.py', 'migrate'])

        # We won't actually create any Employee objects as the error should occur at the query level,
        # not the data level. If necessary, dummy data can be inserted here to help reproduce issues
        # related to data values.
        
        # The part where the issue arises
        Employee.objects.annotate(
            lag=Window(
                expression=Lag('salary', offset=1),
                partition_by=F('department'),
                order_by=[F('salary').asc(), F('name').asc()],
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True),
                output_field=models.BooleanField(),
            ),
        )
        raise AssertionError("NotSupportedError was expected but did not occur.")
    except django.db.utils.NotSupportedError as e:
        # If NotSupportedError is caught, print the expected stacktrace of this issue
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    run_test()
```

This Python script is designed to reproduce the Django issue described, where using window expressions in conditional statements of the `SELECT` clause raises a `NotSupportedError`. It defines an in-memory SQLite database, a simple `Employee` model, and tries to annotate a query set in a way that triggers the reported issue. This script will print out a stacktrace if the error is encountered or if Django somehow supports this operation without raising the expected `NotSupportedError`, it will raise an `AssertionError` indicating the operation unexpectedly succeeded.