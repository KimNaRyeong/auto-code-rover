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

# Define the expression from the zip file
x, y = sp.symbols('x y')
expr = (-2*x**4 - 12*x**3*y - 24*x**2*y**2 - 16*x*y**3 + 8*y**4)/(x**6 + 3*x**5*y + 6*x**4*y**2 + 7*x**3*y**3 + 6*x**2*y**4 + 3*x*y**5 + y**6)

# First simplification step
simplified_expr = sp.simplify(expr)
print("After first simplify:", simplified_expr)

try:
    assert sp.count_ops(simplified_expr) == 7, "Simplify does not perform the ultimate simplification step"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
