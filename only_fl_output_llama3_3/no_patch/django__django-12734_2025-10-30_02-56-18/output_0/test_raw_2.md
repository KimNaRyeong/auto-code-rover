Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.migrations.operations.fields import AlterField
from django.db.migrations.writer import MigrationWriter
from django.core.management.commands.makemigrations import CommandError

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

class AppVersion(models.Model):
    name = models.CharField(max_length=10, primary_key=True)

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=15, primary_key=True)
    app = models.ManyToManyField(AppVersion)

try:
    from django.db import migrations

    class Migration(migrations.Migration):
        dependencies = []

        operations = [
            migrations.AlterField(
                model_name='Vulnerability',
                name='cve_id',
                field=models.CharField(max_length=100, primary_key=True),
            ),
        ]

    writer = MigrationWriter()
    writer.write_migration('0002', Migration)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
```

This script sets up a Django project and models similar to the ones in your issue. It then attempts to run the migration that changes the `cve_id` field's max length from 15 to 100. If the issue is present, an `AssertionError` will be raised, which will be caught and printed with a stack trace.