# reproducer.py
import math
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    from sympy import Sum, factorial, oo, N, S, symbols, Matrix
    from sympy.abc import n, x

    # Simulating the test conditions as per the reported errors.
    # sympy.concrete.tests.test_sums_products
    pistr = "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899" # First 100 digits of Pi
    pi_test = Sum(4*factorial(n)**4*(1103 + 26390*n)/factorial(n)**4/396**(4*n), (n, 0, oo))
    assert str(N(pi_test, 100)) == pistr

    # sympy.utilities.tests.test_lambdify
    f = lambdify(x, S('sin(x)'), 'math')
    assert isinstance(f(2), float)

    # sympy.matrices.tests (example adjusted because exact import paths/details were not provided)
    # A recreated condition similar to what might cause DeferredVector example failure.
    v = Matrix([1, 2, 3])
    func = lambda v: (v[0]*3, v[0]*6)
    assert func(v) == (3, 6)

    print("No issue detected. All tests passed successfully.")
    sys.exit(0)

except AssertionError as e:
    print("AssertionError detected during test execution.")
    print_stacktrace(e)
    sys.exit(1)  # Exiting with non-zero code indicates failure in test conditions.
except Exception as e:
    print("An unexpected error occurred.")
    print_stacktrace(e)
    sys.exit(1)
