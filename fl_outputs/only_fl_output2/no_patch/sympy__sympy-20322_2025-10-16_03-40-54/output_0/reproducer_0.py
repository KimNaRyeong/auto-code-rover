import sympy

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

def test_sympy_behavior():
    x = sympy.symbols('x')
    expr_false = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
    expr_true = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

    # Check if both expressions are simplified to the same result
    try:
        assert str(expr_false) == str(expr_true), "Inconsistent behavior detected."
        print("No issue detected. The behavior is consistent.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_sympy_behavior()
    except AssertionError:
        # Exit with non-zero code if an assertion error is raised
        # Indicating that the issue is present
        import sys
        sys.exit(1)
    # Exit with code 0 to indicate the issue is fixed or not present
    sys.exit(0)
