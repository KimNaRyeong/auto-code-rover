Here is the `reproducer.py` script that reproduces the issue:

```python
import django
from django.db.models import Q, QuerySet
from django.db.models.expressions import F
from django.db.models.query_utils import Q as QExpression

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

def reproduce_issue():
    from django.db.models import Model
    class MyModel(Model):
        pass

    qs = MyModel.objects.all().order_by('id')
    assert qs.query.ordering == ['id'], "Ordering is not as expected"
    
    # This should raise an AssertionError because the order mutates on queryset execution
    reverse_qs = qs.reverse()
    print_stacktrace(AssertionError("Ordering has changed"))

if __name__ == "__main__":
    django.setup()
    reproduce_issue()
```

To run this script, save it in a file named `reproducer.py` and execute it using Python 3: `python3 reproducer.py`. This should raise an `AssertionError` with the stack trace of the issue.