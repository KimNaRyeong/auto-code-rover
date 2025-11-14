from sympy import Range, symbols, Eq
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

x = symbols('x')

try:
    result = Range(3,11,2).as_relational(x)
    assert str(result) == '((x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1))', f"Expected '((x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1))' but got {result}"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
