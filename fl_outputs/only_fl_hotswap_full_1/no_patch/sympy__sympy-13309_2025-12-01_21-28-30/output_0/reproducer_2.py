from sympy import Max, Piecewise, symbols
from sympy.core.expr import Expr
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

a, b = symbols('a b')

expected = Piecewise((a, a > b), (b, True))
actual = Max(a, b).rewrite(Piecewise)

if not isinstance(actual, Expr):
    raise AssertionError(f"Expected {expected} but got {actual} of type {type(actual)}")

if actual != expected:
    raise AssertionError(f"Expected {expected} but got {actual}")
