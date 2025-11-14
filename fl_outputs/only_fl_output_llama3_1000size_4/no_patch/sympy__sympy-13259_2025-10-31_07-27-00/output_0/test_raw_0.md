Here is the reproducer script:

```python
import sympy as sp
from sympy import I, cos, pi, sqrt, asinh, simplify

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
        a = sp.Rational(2)*sp.sqrt(2)*I*sp.cos(sp.pi/6 - I*asinh(5*sp.sqrt(2)/2)/3)/3
        b = a.simplify()
        if not sp.algsys.is_close(a.evalf(), b.evalf()):
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to simplify the expression and check if the result is numerically equal to the original expression. If not, it will print a stack trace of the issue and exit with code 1.