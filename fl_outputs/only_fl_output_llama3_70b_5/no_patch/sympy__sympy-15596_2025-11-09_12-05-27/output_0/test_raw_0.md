Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
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

x = sp.symbols('x')
f = (x-2)/(x**2+1)

try:
    assert sp.degree(f, x) == 2
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
```
This script will try to compute the degree of the rational function `(x-2)/(x**2+1)` with respect to `x` using SymPy's `degree` function. If the result is not 2 (which is the expected correct answer), it will raise an `AssertionError`, print the stack trace, and exit with code 1. If the issue is fixed and the degree is correctly computed, the script will exit with code 0.