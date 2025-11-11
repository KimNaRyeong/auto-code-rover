Here is the `reproducer.py` file that reproduces the issue:

```python
import sympy as sp
from sympy.abc import x
import traceback
import sys

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

try:
    assert str(sp.Poly(x)*x) == "Poly(x**2, x, domain='ZZ')"
    assert str(x*sp.Poly(x)) != "Poly(x*x, x, domain='ZZ')"
    assert str(-2*sp.Poly(x)) == "Poly(-2*x, x, domain='ZZ')"
    assert str(sp.S(-2)*sp.Poly(x)) == "-2*Poly(x, x, domain='ZZ')"
    assert str(sp.Poly(x)*sp.S(-2)) == "Poly(-2*x, x, domain='ZZ')"

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

This script will run the given expressions and check if they produce the expected results. If any of the assertions fail, it will print the stack trace and exit with code 1. Otherwise, it will print a success message and exit with code 0.