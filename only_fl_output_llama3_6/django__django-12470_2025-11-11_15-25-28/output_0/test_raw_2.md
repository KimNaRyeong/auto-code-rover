Here is the reproducer script:

```python
import os
from django.db import models
from django.apps import apps
from django.core.management import execute_from_command_line

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myapp.settings'
    execute_from_command_line(['manage.py', 'shell'])
    from myapp.models import Parent, Child
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

This script sets the DJANGO_SETTINGS_MODULE environment variable to 'myapp.settings', then runs a Django shell using manage.py. It then defines and saves instances of the `Parent` and `Child` models, and attempts to query all parents ordered by their primary key in descending order. If the issue is present (i.e., the ordering is ascending instead of descending), it prints the stack trace and exits with code 1. Otherwise, it prints a success message and exits with code 0.

Please note that this script should be placed in the root directory of your Django project and executed by `python3 reproducer.py`.