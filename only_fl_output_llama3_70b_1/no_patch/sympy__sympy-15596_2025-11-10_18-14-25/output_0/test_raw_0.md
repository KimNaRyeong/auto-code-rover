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
This script defines a rational function `f` and tries to compute its degree using SymPy's `degree` function. If the degree is not correctly computed (i.e., it returns 1 instead of 2), an `AssertionError` is raised, and the script prints the stack trace using the provided `print_stacktrace` function. If the issue is fixed, the script will exit with code 0.