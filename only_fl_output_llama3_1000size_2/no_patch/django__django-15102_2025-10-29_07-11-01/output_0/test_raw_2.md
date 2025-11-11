Here is a revised standalone Python script `reproducer.py` that reproduces the issue:

```python
import os
import sys
from django.core.management import execute_from_command_line

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

def reproduce_issue():
    os.umask(0o77)  # Set umask to 077
    try:
        with open('test.txt', 'w') as f:  # Try to create a file
            pass
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script sets the umask to 077, then tries to create a new file. If an exception is raised during this process (which should be the case due to the read-only permissions), it prints the stack trace and exits with code 1.