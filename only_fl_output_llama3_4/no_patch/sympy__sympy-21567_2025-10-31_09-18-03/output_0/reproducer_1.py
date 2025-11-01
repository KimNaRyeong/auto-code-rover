import sympy as sp
from sympy import *

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

def reproduce_issue():
    x, y = symbols('x y')
    try:
        assert expand_trig(csch(x + y)) != csch(x + y), "Expected different result"
        assert expand_trig(sech(x + y)) != sech(x + y), "Expected different result"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue fixed")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
