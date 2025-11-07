```python
# reproducer.py

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
    from decimal import Decimal
    from django.core.validators import DecimalValidator
    from django.core.exceptions import ValidationError

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
```

To execute this script, you should have Django installed in your Python environment because it utilizes Django's `DecimalValidator` class. If the issue with validating `0E+1` as a decimal in Django 2.0 is present, when you run `python3 reproducer.py`, it will print a stack trace pointing to where the `ValidationError` was raised within Django and then an `AssertionError` will indicate that the validation failed. If the issue is not present (i.e., if Django correctly validates `0E+1` as a decimal), the script will simply print a success message and exit with code 0, indicating the problem is fixed or not present.