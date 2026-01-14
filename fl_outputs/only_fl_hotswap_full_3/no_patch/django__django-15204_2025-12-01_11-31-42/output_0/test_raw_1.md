 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.core.exceptions import ValidationError
from django.forms import DurationField
from django.utils.dateparse import parse_duration

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

def test_duration_field():
    duration_field = DurationField()
    value = 'P3(3D'
    with pytest.raises(ValidationError):
        duration_field.clean(value)

if __name__ == "__main__":
    try:
        test_duration_field()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace of the issue. The script uses the `print_stacktrace` function provided to show the line numbers of the statements clearly. The `test_duration_field` function tests the `clean` method of the `DurationField` class with the input string `'P3(3D'`, which should raise a `ValidationError` due to the broken data. If the issue is fixed, the script should exit with code 0.