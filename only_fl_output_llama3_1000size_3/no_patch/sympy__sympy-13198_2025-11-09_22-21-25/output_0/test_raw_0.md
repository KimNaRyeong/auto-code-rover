Here is the reproducer script:

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
        x, y = sp.symbols('x y')
        z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
        w = sp.expand(z)
        v = sp.factor(w)
        if not sp.simplify(v) == sp.factor(sp.expand(0.0001*x**2 + 0.0005*x*y + 0.0004*y**2)):
            f = StringIO()
            with redirect_stdout(f):
                raise AssertionError("Factorization of trivial polynomial is incorrect")
            print_stacktrace(AssertionError("Factorization of trivial polynomial is incorrect"))
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by factorizing a trivial polynomial. If the factorization is incorrect, it will raise an `AssertionError` and print the stack trace of the error.