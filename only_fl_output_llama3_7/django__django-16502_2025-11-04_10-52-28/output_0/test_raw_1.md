Here is the reproducer script:

```python
import os
import subprocess
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
    try:
        os.chdir('django-test')
        execute_from_command_line(['manage.py', 'runserver'])
        response = subprocess.check_output(['curl', '-iX', 'HEAD', 'http://127.0.0.1:8000/']).decode()
        if '<!DOCTYPE html>' in response:
            raise AssertionError("Expected no HTML body, got it instead")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script creates a new directory 'django-test', starts the development server, sends an HTTP HEAD request to verify that the response body is not empty. If it's not empty, it raises an `AssertionError` with a stack trace.

To run this script, save it as `reproducer.py`, navigate to the root directory of your project, and execute it with `python3 reproducer.py`.