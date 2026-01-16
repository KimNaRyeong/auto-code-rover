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

def test_multiplication_behavior():
    from sympy import symbols, Poly, S

    x = symbols('x')

    try:
        # Poly(x)*x should evaluate the same as x*Poly(x), yielding Poly(x**2, x, domain='ZZ')
        assert Poly(x)*x == Poly(x**2, x, domain='ZZ'), "Poly(x)*x does not evaluate correctly"
        assert x*Poly(x) == Poly(x**2, x, domain='ZZ'), "x*Poly(x) does not evaluate correctly"

        # Test multiplying Poly by -2 and -2 by Poly, both should yield Poly(-2*x, x, domain='ZZ')
        assert -2*Poly(x) == Poly(-2*x, x, domain='ZZ'), "-2*Poly(x) does not evaluate correctly"
        assert Poly(x)*S(-2) == Poly(-2*x, x, domain='ZZ'), "Poly(x)*S(-2) does not evaluate correctly"

        # Test S(-2)*Poly(x) explicitly for completeness; this should also yield Poly(-2*x, x, domain='ZZ')
        assert S(-2)*Poly(x) == Poly(-2*x, x, domain='ZZ'), "S(-2)*Poly(x) does not evaluate correctly"

        print("All multiplication behaviors work as expected.")
    except AssertionError as ae:
        print_stacktrace(ae)
        raise

if __name__ == "__main__":
    test_multiplication_behavior()
