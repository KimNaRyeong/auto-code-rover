import sympy as sp
from sympy import Lambda, symbols, I

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
    try:
        n = symbols('n')
        expr = Lambda(n, 1 + I*n)
        imageset = sp.imageset(expr, sp.Integers)
        assert str(imageset) == '{ⅈ⋅n | n ∊ ℤ}', f"Expected {{ⅈ⋅n | n ∊ ℤ}}, got {imageset}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
