# reproducer.py
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

def test_simplify_pulls_out_constants_from_integral():
    from sympy import symbols, Integral, Sum, simplify
    
    x, y, z, n = symbols('x y z n')
    # Original integral expression that was not simplifying correctly 
    original_expr = Integral(x*y - z, x)

    # Simplified version should have constants pulled out
    expected_simplified_expr = Integral(x*y, x) - z*Integral(1, x)

    # Test for issue with Integral specifically
    integral_simplified_result = simplify(Integral(x*y, (x, 1, n)))
    expected_integral_result = y*Integral(x, (x, 1, n))

    try:
        assert simplify(original_expr) == expected_simplified_expr, "Simplify does not pull constants out of integrals correctly."
        assert integral_simplified_result == expected_integral_result, "Integral simplification does not pull constants outside the integral."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_simplify_pulls_out_constants_from_integral()
    except AssertionError:
        # An AssertionError means the issue is still present.
        exit(1)
    # Exiting with 0 when the issue is fixed.
    exit(0)
