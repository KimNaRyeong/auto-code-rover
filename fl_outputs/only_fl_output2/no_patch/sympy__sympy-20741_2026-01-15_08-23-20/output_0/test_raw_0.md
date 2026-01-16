```python
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

def check_matrix_simplification():
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)
    # Original expressions
    expr1 = -(-A + B) - A + B
    expr2 = (-(-A + B) - A + B).simplify()
    expr3 = (-(-A + B) - A + B).expand()
    expr4 = (-(-A + B) - A + B - Z).simplify()
    expr5 = (-(-A + B) - A + B - Z).expand()

    # Expected result after simplifying or expanding
    expected_expr = -B + A - A + B

    try:
        assert str(expr2) == str(expected_expr), "Simplification failed"
        assert str(expr3) == str(expected_expr), "Expansion failed"
        assert str(expr4) == str(expected_expr), "Simplification with ZeroMatrix failed"
        assert str(expr5) == str(expected_expr), "Expansion with ZeroMatrix failed"
        print("No issues detected. The matrix simplification and expansion works as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        check_matrix_simplification()
    except AssertionError:
        # This indicates an issue was detected
        exit(1)
    else:
        # If no exception was raised, the issue is resolved
        exit(0)
```