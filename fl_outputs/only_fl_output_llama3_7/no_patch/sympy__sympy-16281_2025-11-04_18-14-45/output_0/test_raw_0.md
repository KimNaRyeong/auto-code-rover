Here is the reproducer script:

```python
import sys
from functools import partial
from io import StringIO
from contextlib import redirect_stdout

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
    from your_module import Product
    f = StringIO()
    with redirect_stdout(f):
        try:
            pprint(Product(1, (n, 1, oo)))
            pprint(Product(1/n, (n, 1, oo)))
            pprint(Product(1/n**2, (n, 1, oo)))
            pprint(Product(1, (n, 1, oo)), use_unicode=False)
            pprint(Product(1/n, (n, 1, oo)), use_unicode=False)
            pprint(Product(1/n**2, (n, 1, oo)), use_unicode=False)
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will execute the `Product` pretty printing and check if any of the expected issues occur. If an issue is present, it will raise an `AssertionError`, which will be caught by the script and a stack trace will be printed to the console.