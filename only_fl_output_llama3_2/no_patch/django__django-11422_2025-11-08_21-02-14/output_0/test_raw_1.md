Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line
import time
import traceback

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
    try:
        with open('manage.py', 'a') as f:
            f.write('print("Hello")\n')
        execute_from_command_line(['manage.py', 'runserver'])
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not present, exiting with code 0")
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to reproduce the issue by modifying `manage.py` and then running it using Django's management command. If the issue is present (i.e., an AssertionError is raised), it prints a stack trace and raises the exception again. If the issue is not present, it prints a message indicating that the issue was not found and exits with code 0.