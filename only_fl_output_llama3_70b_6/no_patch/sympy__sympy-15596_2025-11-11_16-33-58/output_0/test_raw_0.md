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
    assert sp.degree(f, x) != 1
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("Issue is fixed!")
```
This script will reproduce the issue by computing the degree of a rational function using SymPy's `degree` function. If the result is incorrect (i.e., 1), it will raise an `AssertionError`, print the stack trace, and exit with code 1. If the issue is fixed, it will simply print "Issue is fixed!" and exit with code 0.