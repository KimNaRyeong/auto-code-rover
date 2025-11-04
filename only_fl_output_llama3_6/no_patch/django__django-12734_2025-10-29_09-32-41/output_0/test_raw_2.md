Here is the reproducer script:

```python
import os
from django.db import models
from django.db.migrations.operations.fields import AlterField
from django.core.management.commands.makemigrations import CommandError
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

def reproduce_issue():
    settings.configure()

    class AppVersion(models.Model):
        name = models.CharField(max_length=15, primary_key=True)

    class Vulnerability(models.Model):
        cve_id = models.CharField(max_length=15, primary_key=True)
        app = models.ManyToManyField(AppVersion)

    operations = [
        AlterField(
            model_name='Vulnerability',
            name='cve_id',
            field=models.CharField(max_length=100, primary_key=True),
        ),
    ]

    try:
        with open('migrations.py', 'w') as f:
            for operation in operations:
                f.write(f"operations = [{operation.__str__()}]\n")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before creating the models and attempting to write the migration operations. This should allow the script to run without raising an error.