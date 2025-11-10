Here is the reproducer script:

```python
import os
from django.db import models
from django.db.models.expressions import F, Value
from django.db.models.query_utils import Q

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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbed.settings')

from django.db.models import OrderBy
from .models import ParentModel, ChildModel

if __name__ == "__main__":
    try:
        order_by = OrderBy(F('expression'))
        ChildModel.objects.order_by(order_by)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected assertion error"
    else:
        print("Issue not present")
        exit(0)
```

This script sets the DJANGO_SETTINGS_MODULE environment variable before importing Django models. This should allow the script to reproduce the issue.