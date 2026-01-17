from sympy import MatrixSymbol, ZeroMatrix, simplify, expand
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

def test_matrix_expression_simplification():
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    expr = (-(-A + B) - A + B).simplify()
    expected = 0*Z  # expecting a simplified expression to zero matrix effectively
    try:
        assert expr == expected, f"Expected {expected}, but got {expr}"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        test_matrix_expression_simplification()
    except AssertionError:
        # An error is expected with the current issue
        print("AssertionError caught as expected due to the current issue.")
        exit(1)  # Exit with error code to indicate the presence of the issue

    print("No issue detected, exiting with code 0.")
    exit(0)
