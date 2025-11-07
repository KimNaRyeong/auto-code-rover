import sympy as sp
from sympy import symbols, tan

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

x = symbols('x')
tan_x = tan(x)

try:
    root1 = sp.RootOf((x**3+x-1), 0)
    assert root1.poly.gen == x

    root2 = sp.RootOf((tan_x**3+2*tan_x-1), 0)
    assert root2.poly.gen == x

    if root2.poly.gen != x:
        raise AssertionError("RootOf might ignore generator")

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
