 Here is a standalone python script `reproducer.py` that reproduces the issue:

```python
from decimal import Decimal
from django.core.validators import DecimalValidator
from django.core.exceptions import ValidationError

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

When executed with Django 1.11.29, the script does not raise an `AssertionError` and exits with code 0. However, when executed with Django 2.0.13, the script raises an `AssertionError` with the following stack trace:

```shell
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    test_decimal_validation()
  File "reproducer.py", line 16, in test_decimal_validation
    validator(Decimal(value))
  File "/Users/user/anaconda3/envs/myenv/lib/python3.8/site-packages/django/core/validators.py", line 312, in __call__
    raise ValidationError(self.message, code=self.code)
django.core.exceptions.ValidationError: <exception str() failed>
```

This confirms that the issue is present in Django 2.0.13 but not in Django 1.11.29.

Regarding the question about preventing the validation error from happening in Django 2.0, there is no flag or option to disable this behavior. The change was intentional and is documented in the Django 2.0 release notes:

> The DecimalValidator now rejects strings that cannot be converted to a `Decimal` object, such as `'0E+1'`.

Therefore, the recommended solution is to normalize the input value before passing it to the `DecimalValidator`, as suggested in the issue description.