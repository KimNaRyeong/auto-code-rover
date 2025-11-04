Here is the reproducer script:

```python
import os
from django.db import models
from django.apps import apps
from django.core.management.commands.makemigrations import CommandError
import sys
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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_related_name_bug.settings'
    from django.core.management import execute_from_command_line
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
    except CommandError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable to point to your project's settings module, then attempts to run `makemigrations` using Django's management command. If an error occurs during this process (i.e., the issue is present), it prints the stack trace and raises an `AssertionError`.