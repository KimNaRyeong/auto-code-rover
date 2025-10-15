from sympy import polylog, Rational, log, pi, nsimplify, expand_func, diff, Symbol, exp_polar

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

def test_polylog_evaluation():
    result = polylog(2, Rational(1,2))
    expected_result = -log(2)**2/2 + pi**2/12
    simplified_result = nsimplify(expand_func(result.evalf()), [pi**2, log(2)**2])
    
    try:
        assert simplified_result == expected_result, "polylog(2, 1/2) evaluation does not match expected."
    except AssertionError as e:
        print_stacktrace(e)
        raise

def test_expand_func_polylog():
    z = Symbol('z')
    result = expand_func(polylog(1, z))
    expected_result = -log(1-z)
    
    try:
        diff_result = expand_func(diff(polylog(1, z) - result, z))
        assert diff_result.simplify() == 0, "expand_func changes the derivative of polylog(1, z)."
    except AssertionError as e:
        print_stacktrace(e)
        raise
    
    try:
        # Check for exp_polar presence, asserting failure if found
        assert not any(isinstance(arg, exp_polar) for arg in result.atoms()), \
            "expand_func introduces unnecessary exp_polar components."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_polylog_evaluation()
    test_expand_func_polylog()
