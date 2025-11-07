Here is the reproducer script:

```python
from django.db import models

def main():
    try:
        class Restaurant(models.Model):
            pass
        
        Restaurant.objects.annotate(
            pizzas_with_toppings_startswith_n=FilteredRelation(
                'pizzas__toppings',
                condition=models.Q(pizzas__toppings__name__startswith='n'),
            ),
        )
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

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

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.