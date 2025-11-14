Here is the reproducer script:

```python
from django.db import IntegrityError, ProgrammingError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import CommandError
import os
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

def main():
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
        django.setup()
        
        makemigrations_command = MakemigrationsCommand()
        makemigrations_command.handle(None, ['app_authors'])
        migrate_command = MigrateCommand()
        migrate_command.handle(None)
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