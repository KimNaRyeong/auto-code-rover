from sympy import Range, symbols, Eq, floor, Mod
import math

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

x = symbols('x')

result = Range(3,11,2).as_relational(x)
try:
    assert str(result) == '(x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1)', f"Expected '(x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1)' but got {result}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed!")
    exit(0)
