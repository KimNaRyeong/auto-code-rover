import sympy as sp
from sympy import Eq, floor, Mod

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
range_obj = sp.Range(3, 11, 2)
relational_expr = range_obj.as_relational(x)

expected_expr = (x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1)

try:
    assert relational_expr == expected_expr
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
