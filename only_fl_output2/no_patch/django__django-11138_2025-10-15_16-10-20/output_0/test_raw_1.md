Certainly! To create a standalone Python file named `reproducer.py` that attempts to reproduce the described issue while handling Django's configuration and database setup properly, follow the structured approach provided below. This script is designed to test specifically the behavior of timezone handling in Django models when querying the database with and without the use of `__date` filter, taking into account the `TIME_ZONE` configuration for the database.

```python
import os
import sys
import django
from django.conf import settings
from django.db import models, connections
from django.utils import timezone
import datetime

# Define a minimal Django configuration
MINIMAL_SETTINGS = {
    'INSTALLED_APPS': ['__main__'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mydatabase',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '3306',
        },
    },
    'USE_TZ': True,
    'TIME_ZONE': 'UTC',  # Default timezone for the project
    'SECRET_KEY': 'fake-key-for-testing',
}

# Define a simple Django model for testing
class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

def configure_django():
    settings.configure(**MINIMAL_SETTINGS)
    django.setup()

    # Run migrations to create the database schema
    with connections['default'].schema_editor() as schema_editor:
        schema_editor.create_model(MyModel)

def test_time_zone_handling():
    # Prepare test data: a datetime object with a specific timezone
    paris_tz = timezone.pytz.timezone('Europe/Paris')
    dt_with_tz = datetime.datetime(2021, 1, 1, 12, 0, tzinfo=paris_tz)

    # Save a model instance using the datetime object
    instance = MyModel.objects.create(my_datetime_field=dt_with_tz)

    # Test retrieval using exact datetime
    assert MyModel.objects.filter(my_datetime_field=dt_with_tz).exists()

    # Test retrieval using the date part of the datetime
    try:
        assert MyModel.objects.filter(my_datetime_field__date=dt_with_tz.date()).exists()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit to indicate the test failed
    else:
        print("Test passed: The issue is not present.")
        sys.exit(0)  # Exit to indicate the test passed

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    import traceback
    try:
        configure_django()
        test_time_zone_handling()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

Before running this script, ensure the parameters in the `MINIMAL_SETTINGS` dictionary (specifically, the database configuration under `DATABASES`) are correctly set up to match your database credentials and location. This example uses MySQL as per the issue's context, but it's crucial to have the MySQL database and user already set up since the script does not handle the creation of the database itself.

This script explicitly configures Django for the test to run, creates the necessary table for `MyModel` without relying on external migrations, inserts a record with timezone information into the database, and then attempts two types of queries to verify if the dates are handled correctly based on the timezone settings. If the `__date` lookup fails to consider the timezone correctly, the script will print the stack trace and exit with code 1, indicating the presence of the issue.