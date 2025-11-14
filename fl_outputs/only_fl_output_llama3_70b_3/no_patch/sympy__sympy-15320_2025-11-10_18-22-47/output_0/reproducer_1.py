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

try:
    assert sp.RootOf(x**3+x-1,0).poly.gen == x
    assert sp.RootOf((x**3+x-1).subs(x,t),0).poly.gen == t
    assert sp.RootOf(sp.tan(x)**3 + 2*sp.tan(x) - 1, 0).poly.gen == sp.tan(x)
    assert sp.RootOf((x**3+2*x-1),0).poly.gen != sp.tan(x)  # This assertion should fail
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
