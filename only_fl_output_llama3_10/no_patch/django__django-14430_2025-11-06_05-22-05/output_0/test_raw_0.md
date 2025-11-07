Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q, Value, Sum, Coalesce

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
    try:
        OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
        assert False, "Expected None"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    reproduce_issue()
```

This script sets up a Django environment and then attempts to execute the aggregation query with an empty list. If the expected `None` value is not returned, it catches the exception and prints the stack trace before raising it again.