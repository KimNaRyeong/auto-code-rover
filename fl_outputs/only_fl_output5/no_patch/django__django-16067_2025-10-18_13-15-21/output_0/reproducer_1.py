# reproducer.py

import os
import django
from django.conf import settings
from decimal import Decimal
from django.core.validators import DecimalValidator
from django.core.exceptions import ValidationError

def setup_django_environment():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
        ],
        USE_I18N=True,
    )
    django.setup()

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

def main():
    setup_django_environment()

    value = '0E+1'
    validator = DecimalValidator(max_digits=8, decimal_places=7)
    try:
        # Validate that 0E+1 is correctly treated as a valid Decimal value.
        validator(Decimal(value))
    except ValidationError as e:
        # The issue is present; print the stack trace and raise AssertionError
        print_stacktrace(e)
        raise AssertionError(f"Validation failed for {value}") from e

    print(f"{value} validated successfully.")

if __name__ == "__main__":
    main()
