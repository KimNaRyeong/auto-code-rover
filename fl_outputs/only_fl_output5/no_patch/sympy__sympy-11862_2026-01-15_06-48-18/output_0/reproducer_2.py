# reproducer.py
def main():
    from sympy import symbols, sqrt, lambdify, N
    import mpmath  # Use mpmath for high precision arithmetic

    # Setup the symbolic expression and its high-precision evaluation
    x = symbols('x')
    g = sqrt(2) - x
    h = g.evalf(64)
    
    # Lambdify the expressions using 'mpmath' to handle high precision
    f1 = lambdify(x, g, modules='mpmath')
    f2 = lambdify(x, h, modules='mpmath')
    
    # Use a high precision value for evaluating the functions
    sqrt2_evaluated = N(sqrt(2), 64)
    
    result1 = f1(sqrt2_evaluated)
    result2 = f2(sqrt2_evaluated)

    # Compare the results against expected precision using mpmath
    expected_precision = mpmath.mpf('0')
    tolerance = mpmath.mpf('1e-64')

    try:
        # Verify if the difference is within the tolerance for both functions
        assert mpmath.fabs(result1 - expected_precision) < tolerance, "f1 results in precision loss"
        assert mpmath.fabs(result2 - expected_precision) < tolerance, "f2 results in precision loss"
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Re-raise the AssertionError to indicate failure

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

if __name__ == "__main__":
    main()
