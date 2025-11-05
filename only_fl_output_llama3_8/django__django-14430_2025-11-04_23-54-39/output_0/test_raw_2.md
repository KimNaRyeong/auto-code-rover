Here is the reproducer script:

```python
from django.db import models
from django.db.models import Q, F, Sum, Value
from django.db.models.functions import Coalesce

def main():
    try:
        result = OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
        if result['test'] is None:
            raise AssertionError("Expected a value, got None")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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
    main()
```

This script sets up a Django project, defines the `OrderItem` model, and then runs one test to reproduce the issue. If this test fails (i.e., if the expected result is not obtained), it prints the stack trace and exits with code 1.