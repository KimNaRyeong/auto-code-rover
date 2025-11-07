# reproducer.py
import os
import django
from django.conf import settings

def setup_django_environment():
    settings.configure(
        DEBUG=True,
        SECRET_KEY='not_so_secret',
        INSTALLED_APPS=[
            # include any apps that your code depends on; for most basic applications, this might not be necessary
        ],
        # Any other settings required for your application to run
        USE_I18N=True,  # If your exception handling relies on internationalization features
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
    from django.core.validators import DecimalValidator
    from django.core.exceptions import ValidationError
    from decimal import Decimal

    value = '0E+1'
    validator = DecimalValidator(8, 7)
    
    try:
        validator(Decimal(value))
    except ValidationError as e:
        print_stacktrace(e)
        raise AssertionError(f"Validation failed for '{value}'. Decimal in scientific notation should be considered valid.") from None
    else:
        print("Validation passed successfully.")

if __name__ == "__main__":
    setup_django_environment()
    main()
