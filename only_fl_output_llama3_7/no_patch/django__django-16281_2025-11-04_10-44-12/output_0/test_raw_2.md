Here is the reproducer script:

```python
import os
from django.core.management import execute_from_command_line
from django.conf import settings
from django.apps import apps
from django.core.exceptions import AppRegistryNotReady
from django.db.models import ManyToManyField, Model
from django.db import IntegrityError, OperationalError

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

def run_migrations():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    settings.configure()
    apps.populate([])
    execute_from_command_line(['manage.py', 'migrate'])

def reproduce_issue():
    try:
        run_migrations()
        class Bar(Model):
            pass
        class Foo(Model):
            bar = models.ManyToManyField('Bar', blank=True)
        run_migrations()
        class Bar(Model):
            pass
        class Foo(Model):
            bar = models.ManyToManyField('Foo', blank=True)
        run_migrations()
        raise AssertionError("Issue not reproduced")
    except (IntegrityError, OperationalError) as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates the necessary models, runs migrations, and then attempts to change the type of the ManyToManyField. If the issue is present, it will raise an `AssertionError` with a stack trace.