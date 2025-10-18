from sympy import Max, Symbol, Piecewise

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

def test_piecewise_rewriting_of_max():
    a, b = Symbol('a'), Symbol('b')
    expected_piecewise_expression = Piecewise((a, a>b), (b, True))
    rewritten_expression = Max(a, b).rewrite(Piecewise)

    try:
        assert rewritten_expression == expected_piecewise_expression, \
            f"Rewritten expression {rewritten_expression} does not match expected {expected_piecewise_expression}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_piecewise_rewriting_of_max()
    except AssertionError:
        # Exit with a non-zero code to indicate failure
        exit(1)
    # Exits with 0 when successful
    print("The issue is fixed.")
    exit(0)
