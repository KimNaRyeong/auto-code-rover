import sympy as sp
from sympy import FiniteSet, Interval

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

try:
    a = FiniteSet(x, y, 2)
    b = Interval(-10, 10)
    result = sp.Complement(a, b)
    assert str(result) == '{x, y} & ~[-10, 10]', f"Expected '{{x, y}} & ~[-10, 10]' but got {result}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
