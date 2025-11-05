Here is the reproducer script:

```python
import os
from django.core.management import execute_from_command_line
from django.db.models import Model, ManyToManyField
from django.db.models.fields.related import RelatedDescriptor
from django.apps import apps
from django.test.utils import CaptureStdout
from django.test.runner import DiscoverRunner

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_related_name_bug.settings'
    execute_from_command_line(['manage.py', 'makemigrations'])

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(0)
```

This script sets the DJANGO_SETTINGS_MODULE environment variable to point to your test project's settings module, then runs `makemigrations` using Django's management command. If an AssertionError is raised during this process (which should happen if the issue is present), it prints the stack trace and exits with code 0.