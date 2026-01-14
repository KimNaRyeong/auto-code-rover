Below is a standalone Python script named `reproducer.py`. It is designed to test the issue where Django's `DecimalValidator` fails to validate `0` in scientific notation (like `0E+1` or `0E+2`). The script will raise an `AssertionError` if the issue is present, and print a stack trace of the issue. If the issue is fixed, the script will exit with code `0` without any error.

```python
import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator
from decimal import Decimal
import os
import sys

# Initialize Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        # Add any necessary apps that might impact the test
    ),
    SECRET_KEY='very-secret-key',
)
django.setup()

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

def test_decimal_validation_zero_in_scientific():
    value = '0E+1'
    validator = DecimalValidator(8, 7)
    try:
        # Attempt to validate decimal value in scientific notation
        validator(Decimal(value))
    except ValidationError as e:
        print_stacktrace(e)
        assert False, "'{}' is an invalid decimal".format(value)

if __name__ == "__main__":
    try:
        test_decimal_validation_zero_in_scientific()
        print("No issues found. Exiting with code 0.")
        sys.exit(0)
    except AssertionError as e:
        print("AssertionError:", str(e))
        sys.exit(1)
```

Remember to have Django installed in your environment where you intend to run this script. If Django is not installed, you can install it by running `pip install django` in your command line or terminal. Adjust the Django settings as necessary for your specific project or environment setup, especially considering `INSTALLED_APPS` and your database configuration in the `settings.configure()` section.