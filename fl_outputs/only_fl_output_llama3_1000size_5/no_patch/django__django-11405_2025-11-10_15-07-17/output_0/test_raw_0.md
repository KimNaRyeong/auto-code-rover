Here is the reproducer script:

```python
import django
from django.db.models import Q, F
from django.db.models.expressions import F as ExpressionF
from django.test.utils import setup_test_environment

setup_test_environment()

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

try:
    from django.db.models.query import QuerySet
    class MyModel(django.db.models.Model):
        pass

    queryset = MyModel.objects.order_by('id').reverse()
    assert not hasattr(queryset, '_orderings'), "Queryset order and Meta.ordering are mutable with reverse."
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script sets up a test environment for Django, defines a simple model `MyModel`, creates a queryset that orders by the `id` field in descending order using the `reverse()` method, and then asserts that the `_orderings` attribute of the queryset is not present. If the assertion fails (i.e., the issue is present), it prints the stack trace and exits with code 1. Otherwise, it exits with code 0.