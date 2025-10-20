# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.db.models import Case, Value, When, F, Window, BooleanField
from django.db.models.functions import Lag

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

# In-memory SQLite database configuration for Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Minimal Django settings required for models and database
settings.configure(
    DATABASES=DATABASES,
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()

class Employee(models.Model):
    name = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=255)

    class Meta:
        app_label = '__main__'

def run_test():
    try:
        execute_from_command_line(['manage.py', 'migrate'])

        # Define the problematic query including the window function.
        queryset = Employee.objects.annotate(
            lag=Window(
                expression=Lag('salary', offset=1),
                partition_by=F('department'),
                order_by=[F('salary').asc(), F('name').asc()],
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True),
                output_field=BooleanField(),
            ),
        )

        # Attempt to evaluate the queryset to trigger the query execution.
        # We do not actually need to iterate over it; just triggering the query planning.
        list(queryset) 

        # If the query executed without raising an exception, we assume the issue is resolved.
        print("The issue appears to be resolved.")
        sys.exit(0)

    except Exception as e:
        print_stacktrace(e)
        # Check if the exception is specifically the one we're interested in (NotSupportedError),
        # or a general AssertionError for any unexpected behavior.
        assert "NotSupportedError" in str(e), "An unexpected exception occurred."
        # If we encounter the expected NotSupportedError, we print the stack trace but don't raise an error
        # because the script's normal behavior is to demonstrate the presence of the issue.

if __name__ == '__main__':
    run_test()
