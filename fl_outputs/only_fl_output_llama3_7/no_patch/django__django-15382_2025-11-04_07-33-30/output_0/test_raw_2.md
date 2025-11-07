Here is the reproducer script:

```python
from django.db import models
from django.db.models import Exists, Q
from django.db.models.expressions import Subquery

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
    class MyModel(models.Model):
        name = models.CharField(max_length=255)

    qs = MyModel.objects.filter(~models.Exists(MyModel.objects.none()), name='test')
    if not str(qs.query).strip():
        raise AssertionError("WHERE block is missing")

    print(str(qs.query))

except Exception as e:
    print_stacktrace(e)
    exit(1)
```

This script should be placed in a file named `reproducer.py` and executed by running `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError`, print the stack trace of the issue, and exit with code 1.