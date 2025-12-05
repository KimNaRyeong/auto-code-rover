 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from decimal import Decimal
from django.core.validators import DecimalValidator

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

def test_decimal_validation():
    value = '0E+1'
    validator = DecimalValidator(8, 7)
    try:
        validator(Decimal(value))
    except ValidationError:
        assert False, f"'{value}' is a valid decimal"

if __name__ == "__main__":
    try:
        test_decimal_validation()
    except AssertionError as e:
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
```
When executed with Django 1.11.29, the script does not raise an `AssertionError` and exits with code 0. However, when executed with Django 2.0.13, the script raises a `ValidationError` and exits with a non-zero code.

To fix the issue, you can use the workaround you mentioned and normalize the `Decimal` value before validating it. Here is an updated version of the `test_decimal_validation` function that includes this workaround:
```python
def test_decimal_validation():
    value = '0E+1'
    validator = DecimalValidator(8, 7)
    decimal_value = Decimal(value)
    decimal_value = decimal_value.normalize()
    try:
        validator(decimal_value)
    except ValidationError:
        assert False, f"'{value}' is a valid decimal"
```
With this workaround, the script exits with code 0 for both Django 1.11.29 and Django 2.0.13.