Here is the reproducer script:

```python
import pickle
from django.db import models
from django.db.models import Value
from django.db.models.query import Row
from django.db.models.expressions import F

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

class ModelA(models.Model):
    value = models.CharField(max_length=12)

try:
    row = ModelA.objects.annotate(id=Value(1)).values_list('id', 'value', named=True).first()
    pickle.dumps(row)
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected Row to be pickleable"
else:
    exit(0)
```

This script creates a simple Django model `ModelA`, uses it to create a query that returns a namedtuple row, and then tries to pickle the row. If the pickling fails (which it should), it prints the stack trace and raises an assertion error.