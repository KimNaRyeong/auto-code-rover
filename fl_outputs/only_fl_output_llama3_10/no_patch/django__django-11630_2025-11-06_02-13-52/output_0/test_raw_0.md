Here is the reproducer script:

```python
import os
from django.db import models
from django.apps import Apps
from django.conf import settings

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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
    apps = Apps(None)
    models.load_app(apps, 'app1')
    models.load_app(apps, 'app2')

    class Model1(models.Model):
        foo = models.CharField(max_length=255, db_table='table_name')

    class Model2(models.Model):
        bar = models.CharField(max_length=255, db_table='table_name')

    try:
        apps.ready()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == '__main__':
    main()

```

This script creates two Django apps (`app1` and `app2`) with models that have the same table name. It then tries to load these models, which should raise an error due to the duplicate table names. The `print_stacktrace` function is used to print the stack trace of this error.