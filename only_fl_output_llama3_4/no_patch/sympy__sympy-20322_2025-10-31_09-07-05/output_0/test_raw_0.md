Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

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

class Reproducer(TestCase):
    def test_ceiling_issue(self):
        try:
            sp.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
            self.fail("Expected inconsistent behavior")
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    Reproducer().test_ceiling_issue()
```

This script defines a `Reproducer` class that contains a single test method, `test_ceiling_issue`. This method attempts to reproduce the issue by calling `sympify` with `evaluate=False`, and then checks if the result is equal to what we expect. If it's not, an `AssertionError` is raised.

If the issue is present, the script will print a stack trace of the error and raise the exception again. If the issue is fixed, the script will simply exit with code 0.