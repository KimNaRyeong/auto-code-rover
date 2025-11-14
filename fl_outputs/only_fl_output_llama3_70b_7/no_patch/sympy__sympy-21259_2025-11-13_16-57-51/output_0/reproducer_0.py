from sympy import Range, symbols, Eq
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

try:
    relational_expr = Range(3,11,2).as_relational(x)
    assert str(relational_expr) == '((3 <= x) & (x <= 9)) & Eq(Mod(x, 2), 1) & Eq(x, floor(x))', f"Expected '((3 <= x) & (x <= 9)) & Eq(Mod(x, 2), 1) & Eq(x, floor(x))' but got {relational_expr}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
