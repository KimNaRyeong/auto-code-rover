Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

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

try:
    execute_from_command_line(['manage.py', 'makemigrations'])
except Exception as e:
    print_stacktrace(e)
    if "fields.E305" in str(e):
        raise AssertionError("Issue is present")
    else:
        sys.exit(0)
```
This script sets up the Django environment, runs the `makemigrations` command, and catches any exceptions that occur. If the exception is a `fields.E305` error, it raises an `AssertionError`. Otherwise, it exits with code 0.

To use this script, create a new Django project with multiple apps, each with a model that has a ManyToManyField with `related_name='+'`. Then, run the script using `python3 reproducer.py`. If the issue is present, the script will raise an `AssertionError` and print a stack trace.