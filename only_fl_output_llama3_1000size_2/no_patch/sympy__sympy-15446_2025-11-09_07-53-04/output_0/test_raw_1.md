Here is the reproducer script:

```python
import sympy as sp
from sympy import latex, MatrixSymbol
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
        x = sp.MatrixSymbol('x', 2, 2)
        y = sp.MatrixSymbol('y', 2, 2)
        expr = (x*sp.Matrix(1) - y).subs(y, -sp.Matrix(1))
        print(latex(expr))
        assert "x(-y)" in latex(expr), "Expected 'x(-y)' but got " + str(latex(expr))
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("Test passed")
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by creating a matrix product and substituting one of the matrices with its negative. It will then check if the expected string "x(-y)" is present in the LaTeX output. If not, it will raise an `AssertionError` and print the stack trace using the provided function.