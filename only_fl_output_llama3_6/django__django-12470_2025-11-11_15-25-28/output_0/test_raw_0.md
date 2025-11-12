Here is the reproducer script:

```python
import os
from django.db import models
from django.apps import apps
from django.test.utils import setup_test_environment

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

setup_test_environment()

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

try:
    from .models import Parent, Child
    parent = Parent()
    child = Child(parent=parent)
    child.save()
    parents = list(Parent.objects.order_by("-pk"))
    assert len(parents) == 1 and parents[0].pk == 1
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present")
exit(0)
```

This script sets up a test environment, defines the `Parent` and `Child` models, saves an instance of each, and then attempts to query all parents ordered by their primary key in descending order. If the issue is present (i.e., the ordering is ascending instead of descending), it prints the stack trace and exits with code 1. Otherwise, it prints a success message and exits with code 0.