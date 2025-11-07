To address the reported issue and ensure the script is standalone without requiring a preset Django project environment, we need to include Django configuration setup directly within the `reproducer.py`. This will bypass the requirement for an external Django settings module or environment variable. Here's a revised version of your script with Django settings configured programmatically to ensure it can run in a standalone fashion:

```python
import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator

from decimal import Decimal
import sys

# Set up Django environment
settings.configure()
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

def test_decimal_validation(value: str, max_digits: int, decimal_places: int):
    validator = DecimalValidator(max_digits, decimal_places)
    try:
        # This tries to validate 'value' which should not raise ValidationError
        validator(Decimal(value))
        print(f"Successfully validated: {value}")
    except ValidationError as e:
        print_stacktrace(e)
        assert False, f"Decimal value '{value}' with scientific notation was incorrectly deemed invalid."

if __name__ == "__main__":
    print("Django version:", django.get_version())
    test_value = '0E+1'
    max_digits = 8
    decimal_places = 7

    try:
        test_decimal_validation(test_value, max_digits, decimal_places)
    except AssertionError as e:
        sys.exit(1)  # Exits with 1 to indicate failure
    else:
        sys.exit(0)  # Exits with 0 to indicate success
```

This script configures Django settings on-the-fly, enabling you to use Django components (like validators) without needing to execute the script within a Django project. It should be noted that for more complex applications or usage scenarios, configuring Django only with `settings.configure()` might not be sufficient, and additional settings (such as database configuration) might be necessary.

The above script should raise an `AssertionError` if the validation fails due to the issue being present, printing the detailed stack trace for the exception. It exits with code 0 if the issue is fixed, indicating successful validation.