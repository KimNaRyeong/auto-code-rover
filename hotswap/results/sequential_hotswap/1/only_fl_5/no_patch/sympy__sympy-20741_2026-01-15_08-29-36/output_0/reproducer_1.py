from sympy import MatrixSymbol, ZeroMatrix, symbols

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

def test_matrix_simplification_issue():
    m, n = symbols('m n')
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    expr_original = -(-A + B) - A + B
    expr_simplified = expr_original.simplify()
    expr_expanded = expr_original.expand()
    expr_simplified_with_z = (-(-A + B) - A + B - Z).simplify()
    expr_expanded_with_z = (-(-A + B) - A + B - Z).expand()

    # Checking the expression simplification
    # The script should catch the issue by checking if the simplification or expansion did not occur as expected
    try:
        assert expr_simplified != expr_original, "The simplified expression should not match the original."
        assert expr_expanded != expr_original, "The expanded expression should not match the original."
        assert expr_simplified_with_z != expr_original, "The simplified expression with ZeroMatrix should not match the original."
        assert expr_expanded_with_z != expr_original, "The expanded expression with ZeroMatrix should not match the original."
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        test_matrix_simplification_issue()
        # If no AssertionError was raised, it means the issue might not be present (or our test missed it)
        print("No Assertion Error: Issue may have been resolved.")
        exit(0)
    except AssertionError:
        # Exiting with a non-zero code to indicate that the script caught the issue
        exit(1)
