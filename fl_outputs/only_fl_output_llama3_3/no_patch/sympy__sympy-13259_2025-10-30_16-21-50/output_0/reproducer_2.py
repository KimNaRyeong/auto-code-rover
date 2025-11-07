import sympy as sp
from sympy import I, sqrt, pi, asinh, cosh

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
    a = sp.sympify('2*sqrt(2)*I*cos(pi/6 - I*asinh(5*sqrt(2)/2)/3)/3')
    b = a.simplify()
    c = a.evalf()
    if not (sp.N(b).evalf() == c):
        raise AssertionError("Simplification failed")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully.")
exit(0)
