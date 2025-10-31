Here is the reproducer script:

```python
import os
import subprocess
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
    try:
        os.system('django-admin startproject django-test')
        os.chdir('django-test')
        process = subprocess.Popen(['python', 'manage.py', 'runserver'])
        output, error = process.communicate(timeout=5)
        if b'<!DOCTYPE html>' in error:
            raise AssertionError("Issue reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script will create a new Django project, run the development server using `subprocess`, and catch any exceptions that occur. If an exception is caught, it will print a stack trace and exit with code 1.