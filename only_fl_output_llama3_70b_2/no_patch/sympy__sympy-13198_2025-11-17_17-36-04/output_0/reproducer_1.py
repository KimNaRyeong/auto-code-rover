import sympy as sp
from sympy import Symbol, Matrix, lambdify

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

x, y = sp.symbols('x y')
z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
w = sp.expand(z)
v = sp.factor(w)

try:
    assert sp.expand(v) == w, "Factoring result is incorrect"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
