Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.core.management.commands.makemigrations import CommandError
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

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

django.setup()

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=15, primary_key=True)
    app = models.ManyToManyField('AppVersion')

Vulnerability._meta.db_table = 'vulnerability'
Vulnerability._meta.get_field('cve_id').max_length = 100
try:
    makemigrations()
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script sets up a Django project, creates the `Vulnerability` model with a many-to-many field to `AppVersion`, changes the length of the `cve_id` field from 15 to 100, and then attempts to run the migration. If the issue is present (i.e., the `cve_id` field length in the `vulnerability_app` table does not change), it prints the stack trace and exits with code 1.