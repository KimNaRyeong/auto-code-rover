Here is the reproducer script:

```python
import os
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

try:
    from models import Parent, Child
except ImportError as e:
    print_stacktrace(e)
    exit(1)

from django.apps import apps

apps.populate(settings='myapp')

Parent.Meta.ordering = ["-pk"]
class Child(Parent):
    pass

assert Child.objects.all().order_by('-pk').query.order_by() == ['-id'], "Incorrect ordering"
```

This script sets up a test environment for Django and then tries to reproduce the issue by querying the `Child` model. If the query does not order by `-id`, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of any exceptions that occur during execution.