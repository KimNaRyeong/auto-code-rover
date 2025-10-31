Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Sum, Count, Value
from django.db.models.functions import Coalesce

def main():
    try:
        # Test with empty list
        result = models.OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
        assert result['test'] is not None, "Expected a value for 'test', but got None"
    except Exception as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up the Django environment and then attempts to execute the aggregation query with an empty list. If the result is `None`, it raises an `AssertionError` with a stack trace.

Please note that this reproducer script assumes you have a model named `OrderItem` in your project, which has a field named `quantity`.