Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
import django
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.models.signals import post_migrate
from django.db.migrations.operations.fields import AddField
from django.db.utils import OperationalError

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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    django.setup()

    class Country(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=50)

    class ModelWithQuotedName(models.Model):
        obj_id = models.IntegerField()
        obj_num = models.CharField(max_length=20, null=True)
        country_id = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='"countries"("country_id")')

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
    except OperationalError as e:
        print_stacktrace(e)
        raise AssertionError("Expected OperationalError")

    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')

if __name__ == '__main__':
    main()
```

This script sets up a test project, defines two models (`Country` and `ModelWithQuotedName`) with quoted names, and then attempts to run the migration. If the issue is present (i.e., an `OperationalError` is raised), it prints the stack trace and raises an `AssertionError`.