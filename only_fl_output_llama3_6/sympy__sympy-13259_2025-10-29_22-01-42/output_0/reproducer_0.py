import sympy as sp
from sympy import I, sqrt, pi, asinh, cosh, simplify

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
    try:
        sp.init_printing(use_latex=False)
        a = 2*sp.sqrt(2)*I*sp.cos(pi/6 - I*asinh(5*sp.sqrt(2)/2)/3)/3
        b = a.simplify()
        assert a.evalf() == b.evalf(), "Simplification failed"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
