Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Coalesce, Value

def main():
    try:
        OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(models.Sum('quantity'), Value(0)))
        assert False, "Expected None"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a Django environment and then attempts to execute the aggregation query with an empty list. If the expected `None` value is not returned, it prints the stack trace of the exception and raises an `AssertionError`.