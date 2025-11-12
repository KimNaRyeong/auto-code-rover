import sympy as sp
from sympy.abc import a, n
import sys
import traceback

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
    from sympy import product, oo, pi
    result = sp.product(1 - a**2 / (n*sp.pi)**2, [n, 1, oo])
    assert result != 0, "product(1 - a**2 / (n*pi)**2, [n, 1, oo]) should not evaluate to 0"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue reproduced successfully. Exiting with code 1.")
sys.exit(1)
