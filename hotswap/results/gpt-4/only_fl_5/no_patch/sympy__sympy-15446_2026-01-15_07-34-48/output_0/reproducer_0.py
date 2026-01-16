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

def test_latex_matrix_product_issue():
    from sympy import MatrixSymbol, latex

    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    latex_str = latex(expr)

    # Check if the issue exists: the resulting latex string
    # should correctly encapsulate -y in parenthesis when multiplied by x
    expected_substr = 'x \\left(- y\\right)'  # Adjust expected substring as per actual correct format
    if expected_substr not in latex_str:
        raise AssertionError(f"Latex printer issue: Expected '{expected_substr}' in '{latex_str}' but not found.")

try:
    test_latex_matrix_product_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with non-zero to indicate failure

print("No issues detected.")
exit(0)  # Exit with zero to indicate success
