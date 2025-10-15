```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.utils import timezone

# Considered necessary setup for Django environment
settings.configure(
    DEBUG=True,
    USE_TZ=True,
    TIME_ZONE='Europe/Paris',  # This is tz1 in the original description
    INSTALLED_APPS=[
        __name__,  # Let Django know about this app (which is this script)
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mydatabase',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',  # Assuming MySQL is hosted locally
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'TIME_ZONE': 'Europe/Paris',  # This is tz2 in the original description
        },
    },
)

# Setting up the Django environment
django.setup()

# Define a model to work with
class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

    class Meta:
        app_label = __name__

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

# Main function to test and reproduce the issue
def main():
    # Create the necessary database tables
    from django.core.management import call_command
    call_command('migrate', '--noinput', run_syncdb=True)

    # Creating a test record
    dt = timezone.make_aware(timezone.datetime(2017, 7, 6, 20, 50))
    MyModel.objects.create(my_datetime_field=dt)

    # Query the record with the aware datetime object to ensure model creation and time zone handling is correct
    assert MyModel.objects.filter(my_datetime_field=dt).exists(), "The first check failed! Datetime object doesn't match."

    # Query the record using a date lookup
    try:
        assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists(), "The date filter lookup failed! Record with matching date not found."
    except Exception as e:
        # If there's an AssertionError, print the stack trace.
        print_stacktrace(e)
        # Re-raise the exception to allow the script to fail
        raise

if __name__ == '__main__':
    try:
        main()
    except AssertionError:
        # Exit with a non-zero code to indicate an error
        os._exit(1)
    # Indicates success (issue is fixed or not present)
    os._exit(0)
```

This script defines a minimal Django project setup within a single Python file, including the database configuration, model definition, and a couple of tests to reproduce the stated behavior for timezone handling in Django models. It uses MySQL as the database backend, assuming MySQL database details are provided correctly and the database is accessible.

- It first creates a model instance with a datetime field set to a timezone-aware datetime object.
- It then checks if the record can be queried directly with the datetime object, expected to succeed.
- Next, it performs a date-based filter operation on the same datetime field, which, according to the issue description, should fail due to incorrect timezone handling. This is where the `AssertionError` is expected when the issue is present.
- If an assertion fails, it prints the stack trace of the exception and exits with code 1. If the script runs successfully to the end, it exits with code 0, indicating the absence of the issue.