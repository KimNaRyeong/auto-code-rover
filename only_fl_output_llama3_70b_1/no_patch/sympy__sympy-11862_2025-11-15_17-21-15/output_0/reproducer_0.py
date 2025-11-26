import sympy as sp
from mpmath import mp

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

def main():
    x = sp.symbols('x')
    g = sp.sqrt(2) - x
    h = g.evalf(64)

    f1 = sp.lambdify(x, g, modules='mpmath')
    f2 = sp.lambdify(x, h, modules='mpmath')

    mp.dps = 64

    try:
        assert abs(f1(mp.sqrt(2)) - f2(mp.sqrt(2))) < 1e-60
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
