Here is the reproducer script:

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
    try:
        os.chdir('django-test')
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    reproduce_issue()
```

This script will change into the `django-test` directory, run the `runserver` command and catch any exceptions that occur. If an exception is caught, it will print the stack trace using the provided function and exit with a non-zero status code. If no exception is caught, it will exit with a zero status code.

Please note that this script should be placed in the root directory of your project.