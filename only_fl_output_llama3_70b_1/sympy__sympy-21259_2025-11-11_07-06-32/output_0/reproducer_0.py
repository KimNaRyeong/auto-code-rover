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
    relational_expr = Range(3, 11, 2).as_relational(x)
    expected_expr = (x >= 3) & (x <= 9) & Eq(x, x // 1) & Eq(x % 2, 1)
    assert relational_expr == expected_expr, f"Expected {expected_expr} but got {relational_expr}"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed!")
sys.exit(0)
