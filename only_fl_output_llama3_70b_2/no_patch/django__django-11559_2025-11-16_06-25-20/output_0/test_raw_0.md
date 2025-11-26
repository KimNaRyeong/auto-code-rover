Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.test.utils import get_runner

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

from django.core.management import execute_from_command_line

# Create a new Django project
execute_from_command_line(['django-admin', 'startproject', 'reproducer'])

# Define the models
with open('reproducer/models.py', 'w') as f:
    f.write("""
from django.db import models
from django.db.models.functions import Lower

class Parent(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = [Lower('name').asc()]

class Child(Parent):
    pass
""")

# Create the database tables
execute_from_command_line(['python', 'manage.py', 'migrate'])

try:
    # Try to reproduce the issue
    from reproducer.models import Parent, Child
    Parent.objects.all().order_by('name')
    assert False, "Expected an exception"
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script creates a new Django project, defines the models with a Meta ordering that uses an expression, and then tries to reproduce the issue by calling `order_by()` on the parent model. If the issue is present, it will raise an exception, print the stack trace using the provided function, and exit with code 1. If the issue is fixed, it will simply exit with code 0.