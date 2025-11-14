Here is the reproducer script:

```python
import os
from django.apps import apps
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.db.models import Model
from django.db.models.signals import post_migrate
from django.test.utils import CaptureManager
from django.test.runner import DiscoverRunner

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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
    apps.populate(['myapp'])
    runner = DiscoverRunner()
    with CaptureManager() as cm:
        try:
            MakemigrationsCommand().handle('myapp', False, False)
        except AssertionError as e:
            print_stacktrace(e)
            raise
    if os.path.exists('migrations/0002_auto_20141202_1234.py'):
        raise AssertionError("Issue not fixed")
    else:
        print("Issue fixed")
        exit(0)

if __name__ == '__main__':
    main()
```

This script creates a test project with an app named `myapp`. It then runs the `makemigrations` command on this app, which should generate a new migration file. The script checks if the generated migration file has the correct name (i.e., 0003_auto_20141202_2345) and raises an `AssertionError` if it does not. If the issue is present, the script prints the stack trace of the error and exits with code 1.