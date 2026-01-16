"""
Standalone script to reproduce the DecimalField max_digits issue in Django with SQLite.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
import decimal

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


# Dynamically configure settings for Django to avoid the need for a separate project
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # Using in-memory database for simplicity
        }
    },
    INSTALLED_APPS=(
        '__main__',  # Register the current file as an app to allow model discovery
    ),
    USE_TZ=True,
)

django.setup()

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

    class Meta:
        app_label = '__main__'


def test_invalid_decimal_query():
    try:
        # Ensuring the table for DecimalModel exists
        execute_from_command_line(['django-admin', 'migrate'])

        # Performing the operation that's expected to raise an exception
        DecimalModel.objects.create(dec_field=1234)  # Within the max_digits limit

        try:
            DecimalModel.objects.get(dec_field='12345')  # Exceeds max_digits
            raise AssertionError("Querying for decimals larger than max_digits should not succeed.")
        except decimal.InvalidOperation:
            # This is the expected outcome given the issue description
            raise
        except DecimalModel.DoesNotExist:
            pass  # This would be correct behavior if the issue did not exist

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected error occurred."


if __name__ == '__main__':
    test_invalid_decimal_query()
