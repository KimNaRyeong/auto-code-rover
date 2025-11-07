```python
# reproducer.py

import os
import django
from django.conf import settings
from django.db import models
from django.db.models import F, Value, Window, Case, When, BooleanField
from django.db.models.functions import Lag
from django.core.exceptions import NotSupportedError


# Minimal Django setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This app
    ),
    USE_TZ=True,
)

django.setup()


# Models definition
class Employee(models.Model):
    name = models.CharField(max_length=128)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=128)

    class Meta:
        app_label = '__main__'


# Function to print stack trace
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
        # Attempt to use a window expression in a conditional statement within the SELECT clause.
        Employee.objects.annotate(
            lag=Window(
                expression=Lag('salary', offset=1),
                partition_by=F('department'),
                order_by=[F('salary').asc(), F('name').asc()],
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True), output_field=BooleanField()
            ),
        )

        # If the operation succeeds without exception, the issue is fixed
        print("The issue is fixed.")
    except NotSupportedError as e:
        # Raise an AssertionError to indicate the issue is present
        print_stacktrace(e)
        raise AssertionError("The issue is still present.")


if __name__ == "__main__":
    reproduce_issue()
```