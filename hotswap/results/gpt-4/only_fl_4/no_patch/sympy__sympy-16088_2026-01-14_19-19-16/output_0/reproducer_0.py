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

def test_simplify_integral_pulls_out_constant():
    from sympy import symbols, Integral, Sum, simplify

    x, y, z, n = symbols('x y z n')
    integral_expr = Integral(x*y-z, x)
    simplified_integral = simplify(integral_expr)
    
    expected_integral = y*Integral(x, x) - z*Integral(1, x)

    sum_expr = Sum(x*y, (x, 1, n))
    simplified_sum = simplify(sum_expr)

    expected_sum = y*Sum(x, (x, 1, n))
    
    try:
        assert simplified_integral == expected_integral, "Simplify did not correctly pull out constant from integral"
        assert simplified_sum == expected_sum, "Simplify did not correctly pull out constant from sum"
        print("Test passed. Issue is fixed or not present.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_simplify_integral_pulls_out_constant()
