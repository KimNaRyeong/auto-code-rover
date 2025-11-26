import sympy as sp
from sympy.abc import a, n

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
    result = sp.product(1 - a**2 / (n*sp.pi)**2, [n, 1, float('inf')])
    assert result != 0, "Product evaluated to 0, expected sinc(a)"
    print("Issue not present")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
