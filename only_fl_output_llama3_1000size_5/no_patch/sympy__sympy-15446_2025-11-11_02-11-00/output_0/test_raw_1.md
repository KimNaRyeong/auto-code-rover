Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp

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
        from sympy import *
        x = sp.MatrixSymbol('x', 2, 2)
        y = sp.MatrixSymbol('y', 2, 2)
        expr = (x*sp.eye(2)*y).subs(y, -y)
        print(sp.latex(expr))
        assert "x(-y)" in str(sp.latex(expr)), "Expected 'x(-y)' but got " + str(sp.latex(expr))
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, execute `python3 reproducer.py` in your terminal. If the issue is present, it will raise an `AssertionError`, print a stack trace, and exit with code 1.