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

def test_refine_understands_complex_arguments():
    from sympy import symbols, Integral, sin, exp, oo, refine, Q
    a, x = symbols('a x')
    J = Integral(sin(x) * exp(-a * x), (x, 0, oo))
    initial_result = J.doit()
    refined_result = refine(initial_result, Q.positive(a))
    try:
        # Example of the issue: refine() does not simplify for real numbers (a is positive)
        assert str(refined_result) != str(initial_result), "refine() does not understand complex argument simplification"
        # Check if `refine` simplified correctly for positive `a`
        piecewise_condition = "2*Abs(arg(a)) < pi"
        if piecewise_condition in str(refined_result):
            raise AssertionError("refine() failed to simplify expression considering 'a' positive")
        # Additional assert to check `refine` on simple expressions
        refined_abs = refine(abs(a), Q.positive(a))
        assert refined_abs == a, "refine(abs(a), Q.positive(a)) should simplify to 'a'"
        
        # Check if refine simplifies arg(a) under assumption Q.positive(a)
        refined_arg = refine(a.arg(), Q.positive(a))
        assert str(refined_arg) != "arg(a)", "refine(arg(a), Q.positive(a)) does not simplify correctly"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_refine_understands_complex_arguments()
    except AssertionError:
        # Test fails, exiting with error
        exit(1)
    # Test passes, all issues are fixed
    print("All tests passed, issue is fixed.")
    exit(0)
