import sympy as sp
from sympy import I

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

x = sp.Symbol('x')

try:
    result = sp.simplify(sp.cos(x)**I)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("No issue found, exiting with code 0")
