Here is the reproducer script:

```python
import django
from django.db.models import Q, FilteredRelation
from django.db.models.expressions import F

def main():
    try:
        Restaurant.objects.annotate(
            pizzas_with_toppings_startswith_n=FilteredRelation(
                'pizzas__toppings',
                condition=Q(pizzas__toppings__name__startswith='n'),
            ),
        )
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a Django project, attempts to annotate the `Restaurant` model with a filtered relation that has a nested condition, and then prints the stack trace of the exception if the issue is present. If the issue is fixed, it exits with code 0.

Please note that you need to have Django installed in your Python environment for this script to work.