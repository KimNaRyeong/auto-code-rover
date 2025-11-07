# reproducer.py

import os
import django
from django.conf import settings
from django.db import models, utils
from django.db.models import F, Value, Window, Case, When, BooleanField
from django.db.models.functions import Lag
from django import setup

# Setup minimal Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # Registering this script as an app
    ),
    USE_TZ=True,
)
setup()


# Defines a simple Employee model
class Employee(models.Model):
    name = models.CharField(max_length=128)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=128)

    class Meta:
        app_label = '__main__'


# Function to print stack trace for exceptions
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
        # Attempt to use a window expression in the SELECT clause using conditional statements
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

        # If the operation succeeds without raising an exception, the issue is likely fixed
        print("The issue is likely fixed.")

    except utils.Error as e:  # Catching a more general exception to ensure we do not miss the specific one
        print_stacktrace(e)
        raise AssertionError("The issue is still present.")


if __name__ == "__main__":
    reproduce_issue()
