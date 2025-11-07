Here is the corrected `reproducer.py` file:
```python
import django
from django.forms import DurationField
from django.utils.dateparse import parse_duration
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    duration_field = DurationField()
    try:
        duration_field.clean('P3(3D')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == '__main__':
    reproduce_issue()
```
This script defines the `print_stacktrace` function and then uses it to print the stack trace when an exception is raised.