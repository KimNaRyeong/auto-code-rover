import sys
import traceback

from sympy import Poly, S, symbols

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols('x')

def test_multiply_poly_by_expression():
    assert Poly(x)*x == x*Poly(x) == Poly(x**2, x, domain='ZZ')
    assert -2*Poly(x) == Poly(-2*x, x, domain='ZZ')
    assert S(-2)*Poly(x) == -2*Poly(x, x, domain='ZZ')
    assert Poly(x)*S(-2) == Poly(-2*x, x, domain='ZZ')

if __name__ == "__main__":
    try:
        test_multiply_poly_by_expression()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
