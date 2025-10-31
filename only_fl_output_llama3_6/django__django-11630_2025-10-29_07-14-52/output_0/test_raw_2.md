Here is the reproducer script:

```python
import os
from django.db import models
from django.db.utils import ProgrammingError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

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
    settings.configure({
        'INSTALLED_APPS': ['app1', 'app2'],
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }
    })

    class App1(models.Model):
        foo = models.CharField(max_length=255, db_table='table_name')

    class App2(models.Model):
        bar = models.CharField(max_length=255, db_table='table_name')

    try:
        from app1.models import App1
        from app2.models import App2
    except ProgrammingError as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

    if os.environ.get('DJANGO_SETTINGS_MODULE'):
        settings.configure()
    else:
        raise ImproperlyConfigured("Requested settings, but settings are not configured.")

if __name__ == "__main__":
    main()
```

This script creates two Django apps with a model each. Both models have the same table name, which should trigger the error when trying to import the models from both apps. The script then prints the stack trace and raises an assertion error if the issue is present.