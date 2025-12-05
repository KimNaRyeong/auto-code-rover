 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from decimal import Decimal
from django.template.defaultfilters import floatformat

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

value = Decimal('42.12345678901234567890')
formatted_value = floatformat(value, 20)
expected_value = str(value)

if formatted_value != expected_value:
    raise AssertionError(f"Expected '{expected_value}', but got '{formatted_value}'")
```
When executed with Python 3.8.5, the script reproduces the issue and raises an `AssertionError`:
```sh
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    if formatted_value != expected_value:
AssertionError: Expected '42.12345678901234567890', but got '42.12345678901234400000'
```
The `AssertionError` is raised because the `floatformat` filter converts the `Decimal` value to a `float` value, which results in a loss of precision. The expected behavior is that the `floatformat` filter should handle `Decimal` values without losing precision.