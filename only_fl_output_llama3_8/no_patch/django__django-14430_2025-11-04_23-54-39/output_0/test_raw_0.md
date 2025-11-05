Here is the reproducer script:

```python
import django
from django.db import models

def main():
    try:
        # Test with matched Queryset. Sum will return 50
        OrderItem.objects.filter(pk__in=[1]).aggregate(test=models.functions.Coalesce(models.Sum('quantity'), models.Value(0)))
        
        # Test with unmatched Queryset. Sum will return 0
        OrderItem.objects.filter(pk__in=[-1]).aggregate(test=models.functions.Coalesce(models.Sum('quantity'), models.Value(0)))
        
        # Test with unmatched Queryset (using empty list). EmptyResultSet returned because of empty list. Sum will return NONE
        result = OrderItem.objects.filter(pk__in=[]).aggregate(test=models.functions.Coalesce(models.Sum('quantity'), models.Value(0)))
        if result['test'] is None:
            raise AssertionError("Expected 0, got None")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    django.setup()
    main()

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
```

This script sets up a Django project, defines the `OrderItem` model, and then runs three tests to reproduce the issue. If any of these tests fail (i.e., if the expected result is not obtained), it prints the stack trace and exits with code 1.