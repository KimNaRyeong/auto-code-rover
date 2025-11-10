Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import django
from django.db.models import Q, QuerySet
from django.db.models.expressions import F

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
    from django.db.models.query import QuerySet
    class MyModel:
        class Meta:
            ordering = ['field']

    queryset = MyModel.objects.all().order_by('field').reverse()
    assert not hasattr(queryset, 'order_by'), "Ordering is mutable"

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
```

To run the script, execute `python3 reproducer.py` in your terminal. If the issue is present, it will raise an `AssertionError`, print a stack trace of the issue, and exit with code 1. If the issue is fixed, it will print "Issue not present" and exit with code 0.