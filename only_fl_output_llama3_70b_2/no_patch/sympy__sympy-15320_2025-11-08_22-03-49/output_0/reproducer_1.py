import sympy as sp

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

x, t = sp.symbols('x t')

root1 = sp.RootOf(x**3+x-1, 0)
assert root1.poly.gen == x

root2 = sp.RootOf((x**3+x-1).subs(x,sp.tan(x)), 0)
try:
    assert root2.poly.gen == x
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

root3 = sp.RootOf(sp.tan(x)**3 + 2*sp.tan(x) - 1, 0)
assert root3.poly.gen == sp.tan(x)

root4 = sp.RootOf((x**3+2*x-1), 0)
try:
    assert root4.poly.gen != sp.tan(x)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
