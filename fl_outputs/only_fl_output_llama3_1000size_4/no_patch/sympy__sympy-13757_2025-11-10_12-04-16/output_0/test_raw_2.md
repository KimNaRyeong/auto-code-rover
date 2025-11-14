Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x

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
        assert str(x*sp.Poly(1)) == "x*Poly(1, x, domain='ZZ')"
        assert str(sp.Poly(1)*x) == "Poly(x, x, domain='ZZ')"
        assert str(-2*sp.Poly(1)) == "Poly(-2, x, domain='ZZ')"
        assert str(sp.S(-2)*sp.Poly(1)) == "-2*Poly(1, x, domain='ZZ')"
        assert str(sp.Poly(1)*sp.S(-2)) == "Poly(-2, x, domain='ZZ')"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script will run the given expressions and check if they produce the expected results. If any of the assertions fail, it will raise an `AssertionError` and print the stack trace.