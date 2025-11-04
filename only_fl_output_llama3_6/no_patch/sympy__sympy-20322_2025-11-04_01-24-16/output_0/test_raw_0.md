Here is the reproducer script:

```python
import sympy
from sympy import ceiling, simplify
from unittest import TestCase
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

class Reproducer(TestCase):
    def test_ceiling_simplify(self):
        sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
        sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

if __name__ == "__main__":
    f = StringIO()
    with redirect_stdout(f):
        try:
            Reproducer().test_ceiling_simplify()
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

    if f.getvalue():
        print("Issue not fixed, reproducer failed")
        exit(1)
    else:
        print("Issue fixed, reproducer passed")
        exit(0)
```

This script defines a `Reproducer` class that contains the test method. The test method attempts to reproduce the issue by calling the sympy functions with and without evaluation. If an `AssertionError` is raised during the execution of the test method, it means the issue is present and the reproducer prints the stack trace and exits with code 1.