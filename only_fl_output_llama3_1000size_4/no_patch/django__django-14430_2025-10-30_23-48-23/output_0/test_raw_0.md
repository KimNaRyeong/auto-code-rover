Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Coalesce, Value
from django.db.models import Sum

def main():
    try:
        # Test with empty list
        result = models.OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
        assert result['test'] is not None, "Expected a value for 'test', but got None"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up the Django environment and then attempts to execute the aggregation query with an empty list. If the result is `None`, it raises an `AssertionError` with a stack trace.