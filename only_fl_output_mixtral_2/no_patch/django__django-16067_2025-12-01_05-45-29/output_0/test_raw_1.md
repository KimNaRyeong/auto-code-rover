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
$ python3.7 -c "import django; django.setup(); exec(open('reproducer.py').read())"
```
However, when executed with Django 2.0.13, the script raises an `AssertionError` and prints a stack trace:
```shell
$ python3.7 -c "import django; django.setup(); exec(open('reproducer.py').read())"
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    test_decimal_validation()
  File "reproducer.py", line 18, in test_decimal_validation
    validator(Decimal(value))
  File "/Users/amokaddim/miniconda3/envs/myenv/lib/python3.7/site-packages/django/core/validators.py", line 312, in __call__
    raise ValidationError(self.message, code=self.code)
django.core.exceptions.ValidationError: <exception str() failed>
```
There is no flag or option in Django 2.0 to prevent this validation error from happening. The recommended solution is to use the workaround of calling `Decimal('0E+1').normalize()` inside the `to_python` method of a custom `DecimalField` subclass. Here is an example:
```python
from django.forms.fields import DecimalField

class CustomDecimalField(DecimalField):
    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, str) and value.endswith('E+1'):
            value = Decimal(value).normalize()
        return value
```
This custom field can be used in place of `DecimalField` to normalize the decimal value before validation.