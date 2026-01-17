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

def test_issue():
    from sympy import sqrt, to_number_field, minimal_polynomial, PurePoly

    b = 1 - sqrt(2)
    a = to_number_field(b)

    # a should be -1 + sqrt(2), but we will check if its minimal polynomial is correct.
    if a != -1 + sqrt(2):
        raise AssertionError("Generated algebraic number is incorrect.")

    # correct minimal polynomial for b
    if minimal_polynomial(b) != PurePoly(_x**2 - 2*_x - 1, _x, domain='QQ'):
        raise AssertionError("Minimal polynomial of b is incorrect.")

    # Checking minimal polynomial of a, where the issue is.
    correct_minpoly_a = minimal_polynomial(-1 + sqrt(2))
    if a.minpoly != correct_minpoly_a:
        raise AssertionError("Minimal polynomial of generated algebraic number is incorrect.")

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1) # Exit with error when issue is present
else:
    print("Issue resolved.")
    exit(0)
