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

def test_issue():
    from sympy import symbols, cos, exp, oo, AccumBounds

    x = symbols('x')

    try:
        # Expression 1 (x + cos(x)).subs(x, oo)
        expr1_result = (x + cos(x)).subs(x, oo)
        # As per issue, this unexpectedly evaluates to oo
        assert expr1_result == oo, f"(x + cos(x)).subs(x, oo) should evaluate to oo, got {expr1_result}"

        # Expression 2 (exp(x) + cos(x)).subs(x, oo)
        expr2_result = (exp(x) + cos(x)).subs(x, oo)
        # Expected AccumBounds but checking against the issue description
        assert expr2_result == AccumBounds(-oo, oo), f"(exp(x) + cos(x)).subs(x, oo) should not evaluate directly to AccumBounds without clear resolution. Result: {expr2_result}"

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError:
        exit(1)
    print("Issue accurately reproduced or has been fixed.")
    exit(0)
