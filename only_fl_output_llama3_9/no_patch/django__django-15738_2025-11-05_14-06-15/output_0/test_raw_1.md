Here is the reproducer script:

```python
import os
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
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

def run_migrations():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
    makemigrations_command = MakemigrationsCommand()
    makemigrations_command.handle(no_input=True, verbosity=0)
    migrate_command = MigrateCommand()
    try:
        migrate_command.handle(verbosity=0)
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    try:
        run_migrations()
    except AssertionError as e:
        raise
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script will run the makemigrations and migrate commands, and if an error occurs during the migration process, it will print a stack trace of the exception.