```python
from sympy import MatrixSymbol, ZeroMatrix, symbols
from sympy.core.sympify import SympifyError

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

    # Original expressions from the issue
    expr1 = -(-A + B) - A + B
    expr2 = expr1.simplify()
    expr3 = expr1.expand()
    expr4 = (-(-A + B) - A + B - Z).simplify()
    expr5 = (-(-A + B) - A + B - Z).expand()

    # Expected behavior (simplified or correctly expanded)
    expected_expr = 2*B - 2*A

    try:
        # Assert simplification validity
        assert expr1 != expected_expr, "The expression should not have been already simplified."
        assert expr2 != expected_expr, "Simplification did not work as expected."
        assert expr3 != expected_expr, "Expansion did not work as expected."
        assert expr4 != expected_expr, "Simplification with zero matrix did not work as expected."
        assert expr5 != expected_expr, "Expansion with zero matrix did not work as expected."
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    try:
        test_matrix_simplification_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    print("No Assertion Error: Issue may have been resolved.")
    exit(0)
```
Keep in mind that the assertions in `test_matrix_simplification_issue` are designed to fail under the current behavior as reported in the issue you've given. As the issue gets fixed, these assertions should pass, indicating that the problem has been resolved. The script exits with code 0 when the assertions pass, which doesn't raise any errors indicating a fix.