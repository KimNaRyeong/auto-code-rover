Here is the reproducer script:

```python
import django
from django.db.models import Q, Case, When, Value, BooleanField
from django.db.models.functions import Coalesce

def main():
    try:
        from myapp.models import User  # Replace 'myapp' with your app name
        User.objects.annotate(
            _a=Case(
                When(~Q(pk__in=[]), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by("-a").values("pk")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected behavior not achieved")

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue by running the same query that is causing the problem. If an exception occurs, it prints the stack trace and raises an `AssertionError`.