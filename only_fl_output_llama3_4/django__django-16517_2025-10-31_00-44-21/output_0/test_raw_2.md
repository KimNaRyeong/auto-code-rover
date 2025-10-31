Here is the reproducer script:

```python
from django.contrib.admindocs.views import view_detail
from django.core.exceptions import Http404
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        view_detail('view:orders.views.Orders')
    except Http404 as e:
        print_stacktrace(e)
        raise AssertionError("Expected 404 not found")
    else:
        print("Issue is fixed, exiting with code 0")
        exit(0)

if __name__ == "__main__":
    main()
```

This script attempts to access the view 'view:orders.views.Orders' using the `ViewDetailView`. If it raises a 404 error, it prints the stack trace and raises an assertion error.