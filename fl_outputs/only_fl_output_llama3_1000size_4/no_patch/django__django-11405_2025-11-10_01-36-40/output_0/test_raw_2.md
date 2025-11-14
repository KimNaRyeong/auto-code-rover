Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import django
from django.db.models import Q, QuerySet
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

def reproduce_issue():
    from django.db.models.query import QuerySet
    class MyModel(QuerySet):
        class Meta:
            ordering = ['field']

    queryset = MyModel().order_by('field').reverse()
    assert not hasattr(queryset, 'order_by'), "Ordering is mutable"

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
```

This script defines a custom QuerySet class `MyModel` with a Meta class that specifies ordering. It then creates an instance of this QuerySet, orders it by 'field', reverses the order, and asserts that the ordering is mutable. If the issue is present, it raises an AssertionError, prints the stack trace, and exits with code 1.