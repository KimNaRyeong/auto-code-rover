Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sp
from sympy import Symbol, Matrix, lambdify
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x, y = sp.symbols('x y')
z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
w = sp.expand(z)
v = sp.factor(w)

try:
    assert sp.expand(v) == w, "Factoring result is incorrect"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not present")
sys.exit(0)
```
This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.