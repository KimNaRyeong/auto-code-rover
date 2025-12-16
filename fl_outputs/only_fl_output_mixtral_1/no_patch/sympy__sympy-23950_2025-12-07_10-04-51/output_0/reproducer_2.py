from sympy import Contains, Piecewise, Reals, symbols
import sys
import traceback

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

try:
    Piecewise((6, Contains(x, Reals)), (7, True))
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    # This should raise an AssertionError
    assert False, "Piecewise should have raised an exception"
