Here is the reproducer script:

```python
import os
import django
from django.core.management import call_command
from django.db.migrations.recorder import MigrationRecorder
from django.conf import settings
from django.apps import apps

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    
    app_label = 'myapp'
    apps.app_configs[app_label] = apps.AppConfig(app_label, 'myapp')
    
    MigrationRecorder.migration_for_app('myapp', 1)
    MigrationRecorder.migration_for_app('myapp', 2)
    
    call_command('makemigrations', 'myapp')
    
    try:
        call_command('makemigrations', 'myapp')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a Django project, creates two migrations for an app named `myapp`, and then calls `makemigrations` twice. The second call should raise an exception if the issue is present, which will be caught and printed with a stack trace.