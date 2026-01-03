from sympy import sqrt, to_number_field, minimal_polynomial, PurePoly
import traceback, sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

b = 1 - sqrt(2)
a = to_number_field(b)
assert minimal_polynomial(b) == a.minpoly, "The minimal polynomials should be the same"
print_stacktrace(AssertionError("The minimal polynomials should not be the same"))
