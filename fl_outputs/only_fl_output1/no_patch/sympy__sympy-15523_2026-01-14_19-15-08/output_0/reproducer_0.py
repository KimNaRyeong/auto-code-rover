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

def test_implicit_multiplication_application():
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.core import Symbol
    
    x = Symbol('x')
    transformations2 = ('implicit_multiplication_application',)
    case = "2x"
    try:
        result = parse_expr(case, transformations=transformations2)
        assert result == 2 * x, f"Expected 2*x, got {result}"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("test_implicit_multiplication_application failed") from e

def test_sympify_keywords():
    from sympy.core.sympify import sympify
    from sympy.core.sympify import SympifyError
    try:
        sympify('lambda')
        raise AssertionError("test_sympify_keywords did not raise SympifyError")
    except SympifyError as e:
        # Expected error, meaning test should pass here. Do avoid False negative, assert specific.
        assert "lambda" in str(e), "SympifyError not raised for 'lambda'"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected error in test_sympify_keywords") from e

if __name__ == "__main__":
    try:
        test_implicit_multiplication_application()
        test_sympify_keywords()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    print("No issues detected.")
    exit(0)
