import django
from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured

def setup_django_environment():
    try:
        # Setup Django environment if it hasn't been done yet
        settings.configure(
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.admin',
            ],
            # Add any other necessary settings for your Django project
        )
        django.setup()
    except ImproperlyConfigured:
        pass  # Django was already set up

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

    setup_django_environment()
    
    value = '0E+1'
    validator = DecimalValidator(max_digits=8, decimal_places=7)
    try:
        # Simulate form validation with a decimal value in scientific notation
        validator(Decimal(value))
        # If it reaches this point, no ValidationError was raised for the problematic value
        print("The issue is fixed. Exiting with code 0.")
    except ValidationError as e:
        print_stacktrace(e)
        raise AssertionError(f"'{value}' should be a valid decimal but raised ValidationError.")

if __name__ == "__main__":
    main()
