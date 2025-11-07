Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import sys
from django.core.management.commands.runserver import CommandError
from django.core.management.commands.runserver import make_settings
from django.core.management.commands.runserver import get_valid_port
from django.core.management.commands.runserver import parse_command_options

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

def run_reproducer():
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'
        from django.core.management import execute_from_command_line
        options = parse_command_options(['runserver', '--nothreading'])
        execute_from_command_line(['manage.py', 'runserver', '--nothreading'])
    except CommandError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    run_reproducer()
```

This script sets up a Django project and runs the `runserver` command with the `--nothreading` option. If the issue occurs, it prints the stack trace and exits with code 1.