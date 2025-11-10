import sympy as sp
from functools import lru_cache

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

try:
    result1 = (x)*sp.Poly(x)
    if str(result1) != "Poly(x**2, x, domain='ZZ')":
        raise AssertionError("Multiplying an expression by a Poly does not evaluate when the expression is on the left side of the multiplication")

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
