"""
Standalone script to demonstrate Django DecimalField NaN issue reproduction.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models

def setup_django_environment():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=('__main__',),
    )
    django.setup()
    # Run migrations to ensure the database is ready for our model.
    execute_from_command_line(['manage.py', 'migrate'])

setup_django_environment()

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)

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

if __name__ == '__main__':
    try:
        # Attempt to store and then retrieve a NaN value in a DecimalField.
        obj = MyModel.objects.create(value=float('nan'))
        obj.refresh_from_db()  # Expected to fail if the issue is present.
        print("No issue detected: Managed to store and retrieve NaN in a DecimalField.")
    except Exception as e:
        print_stacktrace(e)
        # Check specifically for the TypeError related to decimals, raise AssertionError if not found.
        assert "argument must be int or float" in str(e), "Encountered unexpected error."
        # Exiting with status 0 as the script correctly identified the presence of the issue.
        exit(0)
