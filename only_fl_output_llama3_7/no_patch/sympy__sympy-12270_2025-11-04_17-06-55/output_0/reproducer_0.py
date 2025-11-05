import sympy as sp
from sympy import Mul, I

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

def reproduce_bug():
    x, y = sp.symbols('x y')
    expr1 = -2*x - 4*y - 8
    expr2 = expr1.extract_multiplicatively(-2)
    assert expr2 == 1 + 2*I, "Expected 1 + 2*I but got {}".format(expr2)

try:
    reproduce_bug()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue reproduced successfully. Exiting with code 0.")
    exit(0)
