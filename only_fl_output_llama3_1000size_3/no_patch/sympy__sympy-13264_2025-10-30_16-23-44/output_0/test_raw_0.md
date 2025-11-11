Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
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
    try:
        expr = sp.sympify("(x**2 + y**2)**(3/2)")
        simplified_expr = sp.simplify(expr)
        simplified_expr_again = sp.simplify(simplified_expr)
        assert simplified_expr == simplified_expr_again, "Expected the same result after two simplifications"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to simplify an expression using Sympy's `simplify` function, then simplify the result again. If the two results are not equal, it will print a stack trace and raise an `AssertionError`.