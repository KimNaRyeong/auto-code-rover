Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line

def print_stacktrace(e: Exception):
    import traceback
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
        os.chdir('my_project')
        with open("manage.py", mode="r") as stream:
            print(stream.encoding)
        execute_from_command_line(['-X', 'utf8', 'manage.py', 'runserver', '0.0.0.0:8005', '-v3'])
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script changes into the `my_project` directory, opens and prints the encoding of the `manage.py` file, then runs the Django server with the `-X utf8` option. If an `AssertionError` is raised during this process, it prints the stack trace and exits with code 1.