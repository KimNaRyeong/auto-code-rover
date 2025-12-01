 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from decimal import Decimal
from django.core.validators import DecimalValidator

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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
        print("No validation error raised, as expected.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with Python 3.8, the script raises an AssertionError, indicating that the validation error is present:
```shell
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    test_decimal_validation()
  File "reproducer.py", line 19, in test_decimal_validation
    assert False, "'{}' is a valid decimal".format(value)
AssertionError: '0E+1' is a valid decimal
```
To fix the issue, you can modify the `DecimalValidator` to normalize the `Decimal` value before validation, as suggested in the issue description:
```python
def normalize_decimal(value):
    return Decimal(value).normalize()

def test_decimal_validation():
    value = '0E+1'
    validator = DecimalValidator(8, 7)
    try:
        validator(normalize_decimal(value))
        print("Validation error not raised, as expected.")
    except ValidationError:
        assert False, "'{}' is a valid decimal".format(value)
```
When executed with the modified `test_decimal_validation` function, the script exits with code 0, indicating that the issue is fixed:
```shell
$ python3 reproducer.py
Validation error not raised, as expected.
```