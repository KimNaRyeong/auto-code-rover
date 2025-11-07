I apologize for the previous mistake. Here is a new reproducer script that should correctly reproduce the issue:

```python
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

try:
    from django.db.models import F, Value
    from django.db.models.functions import Lag

    class Employee(models.Model):
        pass

    Employee.objects.annotate(
        lag=models.Window(
            expression=models.Lag(expression='salary', offset=1),
            partition_by=F('department'),
            order_by=[F('salary').asc(), F('name').asc()],
        ),
        is_changed=models.Case(
            When(salary=F('lag'), then=Value(False)),
            default=Value(True), output_field=models.BooleanField()
        ),
    )
except django.core.exceptions.NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Expected NotSupportedError")
```

This script should be run with `python3 reproducer.py` and it will reproduce the issue by raising an `AssertionError`.