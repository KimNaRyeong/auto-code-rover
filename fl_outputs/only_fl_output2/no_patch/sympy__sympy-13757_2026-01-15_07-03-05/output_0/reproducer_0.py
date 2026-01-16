from sympy import Poly, symbols, S
from sympy.core.mul import Mul

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

def check_poly_multiplication():
    x = symbols('x')
    try:
        # Test 1: Poly * x
        assert Poly(x) * x == Poly(x**2, x, domain='ZZ'), "Poly(x) * x failed"
        # Test 2: x * Poly
        assert x * Poly(x) == Poly(x**2, x, domain='ZZ'), "x * Poly(x) failed"
        # Test 3: -2 * Poly
        assert -2 * Poly(x) == Poly(-2 * x, x, domain='ZZ'), "-2 * Poly(x) failed"
        # Test 4: S(-2) * Poly
        assert S(-2) * Poly(x) == Poly(-2 * x, x, domain='ZZ'), "S(-2) * Poly(x) failed"
        # Test 5: Poly * S(-2)
        assert Poly(x) * S(-2) == Poly(-2 * x, x, domain='ZZ'), "Poly(x) * S(-2) failed"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    check_poly_multiplication()
    print("No issue detected.")
