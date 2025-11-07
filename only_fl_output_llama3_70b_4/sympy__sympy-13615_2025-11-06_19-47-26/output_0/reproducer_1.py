from sympy import FiniteSet, Interval, symbols
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

x, y = symbols('x y')

try:
    from sympy.sets import Complement
    a = FiniteSet(x, y, 2)
    b = Interval(-10, 10)
    result = str(Complement(a, b))
    assert result == '{x, y} ∩ (-∞, -10] ∪ [10, ∞)' or result == '{x, y} ∩ (-∞, -10] ∪ [10, +∞)'
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed!")
sys.exit(0)
