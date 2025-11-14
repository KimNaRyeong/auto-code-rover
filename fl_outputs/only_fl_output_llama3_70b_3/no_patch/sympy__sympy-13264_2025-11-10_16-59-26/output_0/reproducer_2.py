import sympy as sp

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

# Define the expression
x, y = sp.symbols('x y')
expr = (-4*x**2*y - 8*x*y**2 + 12*x**2 + 16*x*y + 4*y**2)/(x**2 + 2*x*y + y**2)**2

# First simplification step
expr_simplified_once = sp.simplify(expr)

# Second simplification step (should be the same as the first one)
expr_simplified_twice = sp.simplify(expr_simplified_once)

try:
    # Check if the expression is fully simplified (7 ops)
    assert expr_simplified_once.count_ops() == 7, "Simplification did not converge"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
