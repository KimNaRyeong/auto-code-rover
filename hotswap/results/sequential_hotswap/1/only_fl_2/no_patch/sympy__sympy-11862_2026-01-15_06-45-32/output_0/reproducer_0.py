from sympy import symbols, sqrt, N, lambdify
from mpmath import mp

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

def test_precision_loss_with_lambdify():
    x = symbols('x')
    g = sqrt(2) - x
    h = g.evalf(64)  # high-precision float
    f1 = lambdify(x, g, modules='mpmath')
    f2 = lambdify(x, h, modules='mpmath')

    # Test the precision of f1 and f2
    result_f1 = f1(N(sqrt(2), 64)) # Evaluation using sympy's N for 64 digits precision
    result_f2 = f2(N(sqrt(2), 64))

    # Check if the results are inaccurate indicating a precision loss
    try:
        assert mp.almosteq(result_f1, 0, abs_eps=1e-63), "f1 result shows precision loss"
        assert mp.almosteq(result_f2, 0, abs_eps=1e-63), "f2 result shows precision loss"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_precision_loss_with_lambdify()
    except AssertionError:
        exit(1)
    else:
        exit(0)
