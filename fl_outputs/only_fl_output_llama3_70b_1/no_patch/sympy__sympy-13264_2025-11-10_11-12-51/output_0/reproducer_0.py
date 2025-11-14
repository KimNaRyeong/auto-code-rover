import sympy as sp
from sympy.simplify import simplify
from sympy.core.function import count_ops

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

# Define the initial expression
x, y = sp.symbols('x y')
expr = (2*x**2*y + 4*x*y**2 - 2*y**3)/(x**2 + 2*x*y + y**2)**(3/2) + \
       (2*x**2*y - 4*x*y**2 - 2*y**3)/(x**2 - 2*x*y + y**2)**(3/2)

# First simplification
expr_simplified = simplify(expr)
print("First simplification:", expr_simplified)

# Second simplification
expr_simplified_again = simplify(expr_simplified)
print("Second simplification:", expr_simplified_again)

try:
    assert count_ops(expr_simplified) == count_ops(expr_simplified_again)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
