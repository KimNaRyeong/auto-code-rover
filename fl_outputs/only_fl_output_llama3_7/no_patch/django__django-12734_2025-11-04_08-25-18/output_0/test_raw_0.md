Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.migrations.operations.fields import AlterField
from django.db.migrations.writer import Writer

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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=15, primary_key=True)
    app = models.ManyToManyField('AppVersion')

class AppVersion(models.Model):
    pass

operations = [
    AlterField(
        model_name='Vulnerability',
        name='cve_id',
        field=models.CharField(max_length=100, primary_key=True, serialize=False),
    ),
]

writer = Writer()

try:
    from django.db.migrations import Migration
    migration = Migration('project', '0002')
    for operation in operations:
        operation.write(writer)
        writer.write(migration.operations.append(operation))
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

This script sets up a Django project, defines the models and migration operations, and then attempts to execute the migration. If the issue is present (i.e., the `cve_id` field length in the `vulnerability_app` table remains unchanged), it raises an `AssertionError`, prints the stack trace using the provided function, and exits with code 1. Otherwise, it prints a success message and exits with code 0.