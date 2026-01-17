from sympy import symbols, sqrt, lambdify, N
import mpmath

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

def test_precision_loss():
    x = symbols('x')
    g = sqrt(2) - x
    h = g.evalf(64)  # Evaluates the symbolic expression with 64-digit precision

    # Lambdify expressions
    f1 = lambdify(x, g, modules='mpmath')
    f2 = lambdify(x, h, modules='mpmath')

    # Testing for precision loss
    result1 = f1(N(sqrt(2), 64))
    result2 = f2(N(sqrt(2), 64))

    # This should output a very small number close to 0, but not exactly 0 due to computation precision limitations.
    assert abs(result1) < 1e-60, "Unexpected large result from f1, indicating precision loss"

    # Similarly, expect a very small number, essentially 0, from f2
    assert abs(result2) < 1e-60, "Unexpected result from f2, indicating precision loss"

    # If the code gets here, then the precision has not been lost, and the issue might have been fixed
    print("No precision loss detected. Test passed successfully.")

try:
    test_precision_loss()
except AssertionError as e:
    print_stacktrace(e)
    raise e

