import sympy as sp
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
    sys.exit(1)

def idiff(eq, y, x):
    try:
        yp = sp.solve(eq.diff(x), sp.Derivative(y, x))[0].subs({sp.Derivative(y, x): yp})
    except IndexError:
        raise AssertionError("idiff doesn't support Eq, and it also doesn't support f(x) instead of y.")
    except ValueError as e:
        if "expecting x-dependent symbol(s) but got: f(x)" in str(e):
            raise AssertionError("idiff doesn't support f(x) instead of y.")
    
    return yp

if __name__ == "__main__":
    y, x = sp.symbols('y x')
    f = sp.Function('f')

    eq = sp.Eq(sp.exp(y)*y, sp.exp(x)*x)
    try:
        idiff(eq, y, x)
    except AssertionError as e:
        print_stacktrace(e)

    eq = f(x)*sp.exp(f(x)) - x*sp.exp(x)
    try:
        idiff(eq, f(x), x)
    except AssertionError as e:
        print_stacktrace(e)

    eq = y*sp.exp(y) - x*sp.exp(x)
    try:
        idiff(eq, y, x)
    except AssertionError as e:
        print_stacktrace(e)

    print("All tests passed.")
