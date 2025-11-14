from sympy import MatrixSymbol, ZeroMatrix, expand, simplify
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

def check_simplification_issue():
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    # Original expressions and simplification attempts
    original_expr = -(-A + B) - A + B
    simplified_expr = simplify(-(-A + B) - A + B)
    expanded_expr = expand(-(-A + B) - A + B)
    simplified_with_zero = simplify(-(-A + B) - A + B - Z)
    expanded_with_zero = expand(-(-A + B) - A + B - Z)

    # Assertions to check if the simplification is incorrect
    assert str(simplified_expr) == "-B + A -A + B", "Simplification Issue: Expression wasn't simplified correctly."
    assert str(expanded_expr) == "-B + A -A + B", "Expansion Issue: Expression wasn't expanded correctly."
    assert str(simplified_with_zero) == "-B + A -A + B", "Simplification with Zero Issue: Expression wasn't simplified correctly."
    assert str(expanded_with_zero) == "-B + A -A + B", "Expansion with Zero Issue: Expression wasn't expanded correctly."

    return True

try:
    assert check_simplification_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # The script will exit with 1 if the issue is present

# If all assertions pass, or no exception is caught, the issue might be fixed.
print("No issue detected, or the issue has been fixed.")
exit(0)
