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

def test_sympy_without_numpy():
    try:
        # Attempting to import sympy elements that are known to fail without NumPy
        from sympy import Symbol, Catalan, oo, summation, Rational, factorial, S
        from sympy.abc import n, x
        from sympy.functions import sin
        from sympy.matrices import Matrix
        # Replicate one failing expression from each reported test case
        # sympy.concrete.tests.test_sums_products
        pi_series_result = summation( (4 * factorial(n) * (1103 + 26390 * n)) / (factorial(n)**4 * 396**(4*n)), (n, 0, oo))
        assert pi_series_result.evalf(100) == S.Pi.evalf(100), "pi series comparison failed"
        # sympy.integrals.tests.test_quadrature and so on...

        # sympy.utilities.tests.test_lambdify
        f = lambdify(x, sin(x), "math")
        assert isinstance(f(2), float), "lambdify math sin failed"

        # sympy.matrices.matrices.DeferredVector
        def func(v):
            m = Matrix(v)
            return (m[0], m[-1])
        assert func([1, 2, 3]) == (1, 3), "DeferredVector example failed"

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        import numpy
        print("This script is meant to run in an environment where NumPy is not available.",
              "Please ensure NumPy is uninstalled to replicate the issues.", file=sys.stderr)
        sys.exit(1)
    except ImportError:
        test_sympy_without_numpy()
    print("All tests passed successfully.")
    sys.exit(0)
