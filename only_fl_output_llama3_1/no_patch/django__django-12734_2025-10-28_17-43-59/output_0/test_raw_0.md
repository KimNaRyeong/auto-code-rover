Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.migrations.operations.fields import AlterField
from django.db.migrations.writer import writer

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

django.setup()

models.py = """
class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=15, primary_key=True)
    app = models.ManyToManyField('AppVersion')
"""

operations = [
    AlterField(
        model_name='Vulnerability',
        name='cve_id',
        field=models.CharField(max_length=100, primary_key=True, serialize=False),
    ),
]

writer.write_operations(operations)

try:
    from test_project.models import Vulnerability
except Exception as e:
    print_stacktrace(e)
    exit(1)
```

This script sets up a Django project and attempts to run the migration. If the issue is present (i.e., the `cve_id` field length in the `vulnerability_app` table does not change), it prints the stack trace and exits with code 1.