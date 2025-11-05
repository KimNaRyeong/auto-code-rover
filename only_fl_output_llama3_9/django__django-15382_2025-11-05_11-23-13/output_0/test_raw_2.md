Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import django
from django.db import models
from django.db.models import Q, Exists

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
    try:
        django.setup()
        class MyModel(models.Model):
            name = models.CharField(max_length=255)

        qs = MyModel.objects.filter(~Q(name='test'), name='test')
        if not qs.exists():
            raise AssertionError("Expected query to have no results")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up the Django environment using `django.setup()` before defining the `MyModel` class and attempting to filter the queryset. If the resulting query has no results, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of any exceptions that occur during execution.