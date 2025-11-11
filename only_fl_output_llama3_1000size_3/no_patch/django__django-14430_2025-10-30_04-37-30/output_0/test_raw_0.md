Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Sum, Value, F, Q
from django.db.models.functions import Coalesce

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

def main():
    try:
        OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected Coalesce in Aggregations not to be ignored when EmptyResultSet returned")

if __name__ == "__main__":
    main()
```

This script will run the aggregation query with an empty list and catch any exceptions that are raised. If an `AssertionError` is expected, it will print the stack trace of the exception and raise the error.