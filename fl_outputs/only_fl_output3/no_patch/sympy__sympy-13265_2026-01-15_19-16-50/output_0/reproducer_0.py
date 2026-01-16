from sympy import exp, simplify, Matrix, I, cos, sin
from sympy.simplify.fu import fu
from sympy.simplify.sqrtdenest import sqrtdenest
from sympy.simplify.trigsimp import trigsimp

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

def check_simplicity():
    # Original expression with sin represented as exponentials
    expr = exp(Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]))
    simplified_expr = simplify(expr)
    # Use different simplification methods
    fu_simplified = fu(simplified_expr)
    sqrtdenest_simplified = sqrtdenest(fu_simplified)
    trigsimp_simplified = trigsimp(sqrtdenest_simplified)

    # Expected simplification result based on the issue's description
    expected_sin_expr = sin(1)

    # Extracting the problematic expression from the simplified matrix.
    # In the example, the issue was observed in the matrix component
    # that was expected to be sin(1).
    sin_expr_found = trigsimp_simplified[1, 0]

    try:
        # Checking if the expression for `sin(1)` is correctly recognized.
        # This is based on the description issue where `sin(1)` is expected
        # but not properly simplified/recognized.
        assert sin_expr_found == expected_sin_expr, "Simplification failed to produce correctly recognized `sin(1)`"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        check_simplicity()
    except AssertionError:
        exit(1)
    print("Issue is fixed.")
    exit(0)
