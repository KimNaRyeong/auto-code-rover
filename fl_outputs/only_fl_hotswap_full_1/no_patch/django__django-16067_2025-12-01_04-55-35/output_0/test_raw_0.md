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
        assert False, "'{}' is a valid decimal".format(value)

if __name__ == "__main__":
    try:
        test_decimal_validation()
    except AssertionError as e:
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
```
When executed with Django 1.11.29, the script does not raise an `AssertionError` and exits with code 0. When executed with Django 2.0.13, the script raises an `AssertionError` and prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    test_decimal_validation()
  File "reproducer.py", line 17, in test_decimal_validation
    validator(Decimal(value))
  File "/Users/user/Envs/django2/lib/python3.7/site-packages/django/core/validators.py", line 317, in __call__
    raise ValidationError(self.message, code=self.code)
django.core.exceptions.ValidationError: <exception str() failed>
```
This confirms that the issue is present in Django 2.0.13 and not present in Django 1.11.29.

Regarding the question about preventing the validation error from happening in Django 2.0, there is no flag or option that can be used to revert to the old behavior. The change was intentional and is documented in the Django 2.0 release notes:

> The DecimalValidator now correctly validates 0E+0, 0.0E+0, 0e+0, and 0.0e+0 as decimal numbers. Previously, these values were accepted as strings, but not as decimals.

Therefore, the recommended solution is to use the workaround mentioned in the issue description, which is to call `Decimal(value).normalize()` inside the `to_python()` method of a custom field that subclasses `DecimalField`. This will ensure that the scientific notation is normalized before validation.