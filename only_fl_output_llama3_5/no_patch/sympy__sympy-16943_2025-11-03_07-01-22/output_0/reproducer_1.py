import sympy as sp
from sympy import Symbol, fps
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

def reproduce_issue():
    x = Symbol('x')
    p = fps(x ** 2)
    try:
        p[0]
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue #12310: sympy.fps doesn't always return a formal power series")

if __name__ == "__main__":
    reproduce_issue()
    sys.exit(0 if not hasattr(sys, 'last_exception') else 1)
