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

def test_substitution_issue():
    from sympy import symbols, cos, exp, oo

    x = symbols('x')
    expr1 = x + cos(x)
    expr2 = exp(x) + cos(x)

    result1 = expr1.subs(x, oo)
    result2 = expr2.subs(x, oo)
    
    try:
        assert result1 == oo, "First expression does not evaluate to oo"
        assert result2.is_infinite, "Second expression does not evaluate to an infinite bound"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_substitution_issue()
        print("All checks passed!")
    except AssertionError:
        # If an AssertionError is caught, exit with a non-zero status code to indicate failure
        import sys
        sys.exit(1)
