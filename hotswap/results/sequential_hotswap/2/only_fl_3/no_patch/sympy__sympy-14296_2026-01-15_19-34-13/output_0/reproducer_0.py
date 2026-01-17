from sympy import sqrt, minimal_polynomial, to_number_field
from sympy.abc import x

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

def test_algebraic_number_sign_issue():
    try:
        b = 1 - sqrt(2)
        a = to_number_field(b)

        # Checks if `a` is correctly generated
        assert str(a) == '-1 + sqrt(2)', "Generated algebraic number does not have the expected form."

        # Check if `minimal_polynomial(a)` returns the correct polynomial
        assert minimal_polynomial(a) == minimal_polynomial(-1 + sqrt(2)), "Minimal polynomials do not match."

        # If the minimal polynomial is the same as `b.minpoly`, it indicates the issue is still present
        # as it should have been different for `a`.
        assert minimal_polynomial(a) != a.minpoly, "Minimal polynomial of `a` incorrectly matches `a.minpoly`."

    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_algebraic_number_sign_issue()
    print("No issue detected.")
