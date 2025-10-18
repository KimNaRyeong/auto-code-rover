import sympy
from sympy.abc import x

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

def test_sympify_simplify_behavior():
    expr_without_evaluation = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
    expr_with_evaluation = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

    try:
        assert str(expr_without_evaluation) == str(expr_with_evaluation), "Inconsistent simplify behavior with ceiling"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    print("Test passed: The issue is fixed or cannot be reproduced.")

if __name__ == "__main__":
    test_sympify_simplify_behavior()
