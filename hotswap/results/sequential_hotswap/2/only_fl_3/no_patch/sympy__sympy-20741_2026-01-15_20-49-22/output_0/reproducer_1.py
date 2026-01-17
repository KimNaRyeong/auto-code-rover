from sympy import MatrixSymbol, ZeroMatrix, symbols
from sympy.abc import m, n

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

def test_matrix_expression_issue():
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    expr = -(-A + B) - A + B
    simplified_expr = expr.simplify()
    expanded_expr = expr.expand()

    # Testing for no change after simplification or expansion as reported
    try:
        assert str(simplified_expr) == "-(-A + B) - A + B", "Simplified expression should not change."
        assert str(expanded_expr) == "-B + A - A + B", "Expanded expression should show expanded form."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_matrix_expression_issue()
        # If no exception is raised, the issue is considered not reproduced (i.e., potentially fixed).
        print("No issue detected.")
    except AssertionError:
        # Exiting with code 1 indicates the presence of the issue.
        import sys
        sys.exit(1)
