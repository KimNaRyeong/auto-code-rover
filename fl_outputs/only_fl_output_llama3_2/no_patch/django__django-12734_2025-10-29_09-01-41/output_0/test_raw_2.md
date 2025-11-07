Here is the reproducer script:

```python
import os
import django
from django.db import models

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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
django.setup()

class AppVersion(models.Model):
    name = models.CharField(max_length=10, primary_key=True)

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=15, primary_key=True)
    app = models.ManyToManyField(AppVersion)

try:
    from test_project.models import Vulnerability
except Exception as e:
    print_stacktrace(e)
    exit(1)

assert Vulnerability._meta.get_field('cve_id').max_length == 100, "cve_id field length was not changed"

os.system("python manage.py makemigrations")
os.system("python manage.py migrate")

try:
    from test_project.models import Vulnerability
except Exception as e:
    print_stacktrace(e)
    exit(1)

assert Vulnerability._meta.get_field('cve_id').max_length == 100, "cve_id field length was not changed"

print_stacktrace(AssertionError("Expected cve_id field length to be 100"))
exit(0)
```

This script sets up a simple Django project with two models: `AppVersion` and `Vulnerability`. It then attempts to run the migration that changes the `cve_id` field's maximum length. If the issue is present (i.e., the field's length remains unchanged), it prints the stack trace and exits with code 1.