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
expr = sp.sympify("...")  # Replace with the actual huge expression (675 ops)

# First simplification step
simplified_expr = sp.simplify(expr)

# Second simplification step to reproduce the issue
final_expr = sp.simplify(simplified_expr)

try:
    assert sp.count_ops(final_expr) == 7, "Simplification did not reach the expected result"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
