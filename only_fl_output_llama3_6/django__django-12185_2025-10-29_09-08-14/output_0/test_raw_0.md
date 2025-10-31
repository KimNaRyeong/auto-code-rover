Here is the reproducer script:

```python
import django
from django.db.models import F, Value, BooleanField
from django.db.models.window import Window, Lag
from django.db.models.expressions import Case, When

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
    from django.db.models import Q
    Employee = type('Employee', (object,), {'objects': lambda self: None})
    Employee.objects.annotate(
        lag=Window(
            expression=Lag(expression='salary', offset=1),
            partition_by=F('department'),
            order_by=[F('salary').asc(), F('name').asc()],
        ),
        is_changed=Case(
            When(salary=F('lag'), then=Value(False)),
            default=Value(True), output_field=BooleanField()
        ),
    )
except django.core.exceptions.NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Expected NotSupportedError")
```

This script should be run with `python3 reproducer.py` and it will reproduce the issue by raising an `AssertionError`.