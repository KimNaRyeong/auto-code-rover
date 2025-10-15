"""
reproducer.py

A standalone script to reproduce the issue where chaining select_related mutates the original QuerySet.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Configure Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=(
        '__main__',
    ),
    USE_TZ=True,
)

django.setup()

from django.db import models


class ModelA(models.Model):
    pass


class ModelB(models.Model):
    pass


class ModelC(models.Model):
    model_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)
    model_b = models.ForeignKey(ModelB, on_delete=models.CASCADE)


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


def main():
    # Create the tables in the database
    execute_from_command_line(['manage.py', 'migrate'])

    try:
        query_1 = ModelC.objects.select_related('model_a')
        print('QUERY 1:', str(query_1.query))
        query_2 = query_1.select_related('model_b')
        print('QUERY 2:', str(query_2.query))
        print('QUERY 1 AGAIN:', str(query_1.query))

        # Checking if the bug is present
        assert str(query_1.query) != str(query_2.query), "The original QuerySet was mutated after chaining select_related."

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No issue detected: The original QuerySet remains unmutated after chaining select_related.")
        sys.exit(0)

if __name__ == '__main__':
    main()
