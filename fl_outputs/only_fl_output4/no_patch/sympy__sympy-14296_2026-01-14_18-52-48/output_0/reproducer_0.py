# reproducer.py
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

try:
    b = 1 - sqrt(2)
    a = to_number_field(b)
    assert str(a) == "-1 + sqrt(2)", "Generator not created with expected sign."

    min_poly_b = minimal_polynomial(b, x)
    assert min_poly_b == x**2 - 2*x - 1, "Minimal polynomial of b is incorrect."

    min_poly_a = minimal_polynomial(a, x)
    # This assertion fails due to the issue described:
    assert min_poly_a != x**2 - 2*x - 1, "Minimal polynomial of a should not be the same as min_poly_b."

    correct_min_poly_a = minimal_polynomial(-1 + sqrt(2), x)
    assert min_poly_a == correct_min_poly_a, f"Minimal polynomial of a is incorrect. Expected {correct_min_poly_a}, got {min_poly_a}"

except AssertionError as e:
    print_stacktrace(e)
    raise e

print("No issue detected.")
