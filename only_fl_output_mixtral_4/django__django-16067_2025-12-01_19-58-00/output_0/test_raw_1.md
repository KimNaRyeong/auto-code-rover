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
When executed with Django 1.11.29, the script does not raise an `AssertionError` and exits with code 0:
```shell
$ python3.8 -c "import sys; sys.path.append('path/to/django/1.11.29'); import reproducer"
```
When executed with Django 2.0.13, the script raises an `AssertionError` and prints a stack trace:
```shell
$ python3.8 -c "import sys; sys.path.append('path/to/django/2.0.13'); import reproducer"
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    test_decimal_validation()
  File "reproducer.py", line 17, in test_decimal_validation
    validator(Decimal(value))
  File "/path/to/django/2.0.13/django/core/validators.py", line 313, in __call__
    raise ValidationError(self.message, code=self.code)
django.core.exceptions.ValidationError: ['“0E+1” could not be converted to a decimal.’]
```
As for preventing the validation error from happening in Django 2.0, there is no flag or option to disable this behavior. The change was intentional and is documented in the release notes for Django 2.0.

The recommended solution is to normalize the decimal value before validating it, as you mentioned in your issue description. Here is an example of how to do this:
```python
def to_python(self, value):
    value = super().to_python(value)
    if isinstance(value, str):
        value = Decimal(value).normalize()
    return value
```
This code overrides the `to_python` method of the `DecimalField` class and normalizes the decimal value if it is a string. This ensures that the value is validated correctly, even if it is in scientific notation.