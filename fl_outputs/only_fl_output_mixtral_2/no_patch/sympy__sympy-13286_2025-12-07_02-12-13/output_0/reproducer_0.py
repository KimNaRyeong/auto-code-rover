from sympy import *
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = Symbol('x')

# The periodicity function should return the period of the given expression
# However, it returns 2*pi instead of pi for Abs(sin(x))
assert periodicity(Abs(sin(x)), x) == pi, "periodicity(Abs(sin(x)), x) returns 2*pi instead of pi"

print("Test passed")
sys.exit(0)
