Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Coalesce, Value

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
    django.setup()
    
    class OrderItem(models.Model):
        quantity = models.IntegerField()

    try:
        result1 = OrderItem.objects.filter(pk__in=[1]).aggregate(test=Coalesce(models.Sum('quantity'), Value(0)))
        assert result1['test'] == 50
        
        result2 = OrderItem.objects.filter(pk__in=[-1]).aggregate(test=Coalesce(models.Sum('quantity'), Value(0)))
        assert result2['test'] == 0
        
        result3 = OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(models.Sum('quantity'), Value(0)))
        if result3['test'] is not None:
            print_stacktrace(AssertionError("Expected 'test' to be None"))
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines an `OrderItem` model with a `quantity` field, and then performs the same queries as described in the issue. It asserts that the results are as expected, and if any of the assertions fail, it prints the stack trace using the provided function.