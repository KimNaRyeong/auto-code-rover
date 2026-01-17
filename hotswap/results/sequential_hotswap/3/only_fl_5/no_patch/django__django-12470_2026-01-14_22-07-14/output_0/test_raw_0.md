```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

# Minimal Django configuration for running this script as a standalone script.
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # Use an in-memory SQLite database
        }
    },
    INSTALLED_APPS=[
        __name__,  # Register this module as a Django app to create the model table.
    ],
    USE_I18N=False,
    USE_L10N=False,
    USE_TZ=False,
)
django.setup()

# Define the models as per the issue description
class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

# Function to migrate models and create the database schema.
def migrate_and_create():
    from django.core.management import call_command
    call_command('makemigrations', __name__, verbosity=0)
    call_command('migrate', verbosity=0)

def test_ordering():
    # Create a couple of Child instances to test the ordering
    Child.objects.create()
    Child.objects.create()
    query = str(Child.objects.all().query)
    expected_order = 'DESC'  # We expect the IDs to be ordered in descending order
    if 'ASC' in query:
        raise AssertionError('Query is ordered ASC but expected DESC')

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

if __name__ == '__main__':
    try:
        migrate_and_create()
        test_ordering()
        print("Test passed: Issue not present or has been fixed.")
    except Exception as e:
        print_stacktrace(e)
        os._exit(1)  # Use os._exit to exit the program with status 1
```

This script is a standalone Python file that reproduces the issue as described. It performs the following actions:

1. Configures a minimal Django environment for the script to run independently.
2. Defines the `Parent` and `Child` models as described in the issue, with the ordering specified in the `Parent`'s meta class.
3. Adds a minimal setup with an in-memory SQLite database and dynamically creates migrations and tables for these models.
4. Implements a test function `test_ordering` that tries to detect if the queryset's ordering is incorrect based on the issue description.
5. Uses the provided `print_stacktrace` function to print the stack trace if the assertion fails, indicating the presence of the issue.
6. Exits with code 0 if the issue is not present or has been fixed; otherwise, it exits with code 1.