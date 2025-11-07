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

def test_polylog_2_issue():
    from sympy import polylog, Rational, log, pi, nsimplify, expand_func, Symbol

    # First issue reproduction attempt
    try:
        result = polylog(2, Rational(1, 2)).expand(func=True)
        expected_result = -log(2)**2/2 + pi**2/12
        # Calculating numerical approximation to compare with expected numerical result
        approx_result = result.evalf()
        expected_approx_result = expected_result.evalf()
        assert approx_result == expected_approx_result, f"Expected approx {expected_approx_result}, got {approx_result}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def test_polylog_1_issue():
    from sympy import polylog, symbols, expand_func, log, diff, exp_polar, I, simplify

    z = symbols('z')
    # Second issue reproduction attempt
    try:
        expanded = expand_func(polylog(1, z))
        expected = -log(1 - z)
        # Verifying if the expression unnecessarily includes exp_polar
        if expanded.has(exp_polar):
            raise AssertionError("Expanded polylog(1, z) includes unexpected exp_polar.")

        # Ensuring the derivative does not change unexpectedly
        derivative_original = diff(polylog(1, z), z)
        derivative_expanded = diff(expanded, z)
        if not simplify(derivative_original - derivative_expanded) == 0:
            raise AssertionError("Derivative mismatch after expansion.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

try:
    test_polylog_2_issue()
    test_polylog_1_issue()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("All checks passed successfully.")
exit(0)
