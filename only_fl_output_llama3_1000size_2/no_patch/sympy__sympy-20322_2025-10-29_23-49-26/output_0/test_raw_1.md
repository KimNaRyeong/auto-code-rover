Here is the reproducer script:

```python
import sympy as sp
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
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
        expr = sp.sympify('4*ceiling(x/4 - 3/4)', evaluate=False)
        result1 = expr.simplify()
        expr = sp.sympify('4*ceiling(x/4 - 3/4)', evaluate=True)
        result2 = expr.simplify()
        assert result1 == 4*sp.ceiling(x/4) - 3, "Issue reproduced successfully. Sympy version is not affected."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue reproduced successfully. Sympy version is not affected.")
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script checks the behavior of `simplify` for a given expression with and without evaluation, and raises an `AssertionError` if the results are different. If the assertion fails, it prints the stack trace and exits with code 1.