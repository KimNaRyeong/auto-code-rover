Here is the reproducer script:

```python
import os
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

def main():
    class AppVersion(models.Model):
        name = models.CharField(max_length=15, primary_key=True)

    class Vulnerability(models.Model):
        cve_id = models.CharField(max_length=15, primary_key=True)
        app = models.ManyToManyField(AppVersion)

    writer = Writer()
    operations = [
        AlterField(
            model_name='Vulnerability',
            name='cve_id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]

    try:
        with open('migrations.py', 'w') as f:
            writer.write_operations(operations, f)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script creates a minimal Django project and attempts to generate the migration file that reproduces the issue. If an exception occurs during this process (which should be the case if the issue is present), it prints the stack trace using the provided function, exits with code 1, indicating that the issue was found.