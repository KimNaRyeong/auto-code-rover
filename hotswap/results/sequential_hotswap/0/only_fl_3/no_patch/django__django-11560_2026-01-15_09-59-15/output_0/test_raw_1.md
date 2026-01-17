To address the issue identified in the previous attempt, I've refined the approach to ensure that Django is appropriately set up and configured within the standalone script. This refined script should correctly initialize Django's settings before attempting to define models or execute queries, which was the source of the `ImproperlyConfigured` error.

Please note, to test this script effectively, ensure Django is installed in your environment and use a database backend supported by Django that does not require additional setup for simple operations (SQLite is used here because it requires no setup). Here's the revised script:

```python
import django
from django.conf import settings
from django.core.management import execute_from_command_line
import os
import sys

# Configure Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        '__main__',
    ),
    USE_TZ=True,
)

django.setup()

from django.db import models
from django.db.models.functions import ExtractYear

# Define your models here
class MyModel(models.Model):
    duration = models.DurationField()

# Initialize Django command line utilities to setup the database
execute_from_command_line(['manage.py', 'migrate'])


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

# Main function to reproduce the issue
def main():
    try:
        # Attempt the query that should reproduce the issue
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
        # If no error is raised, assume the issue is fixed
        print("The issue seems to be fixed.")
    except Exception as e:
        print_stacktrace(e)
        # Raise AssertionError to indicate the presence of the issue
        raise AssertionError("The issue is still present.")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as err:
        print(f"Assertion failed: {err}")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
```

This script includes the necessary Django setup at the beginning to prevent the `ImproperlyConfigured` error. It defines a minimal Django model `MyModel` with a `DurationField`, and then attempts to reproduce the issue described by annotating with `ExtractYear` and filtering. The presence of the bug will trigger an exception, captured and displayed by the `print_stacktrace` function, followed by an `AssertionError` indicating the issue persists. If the operation succeeds without raising an exception, it indicates the issue has been resolved.