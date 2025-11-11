Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line
from django.db.utils import IntegrityError, ProgrammingError
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

def main():
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
        execute_from_command_line(['manage.py', 'makemigrations', 'app_authors'])
        execute_from_command_line(['manage.py', 'migrate'])
    except (IntegrityError, ProgrammingError) as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
```

This script sets up a Django project, runs the makemigrations and migrate commands, and catches any IntegrityError or ProgrammingError exceptions that are raised. If an exception is caught, it prints the stack trace using the provided `print_stacktrace` function and raises an AssertionError to indicate that the issue has been reproduced.