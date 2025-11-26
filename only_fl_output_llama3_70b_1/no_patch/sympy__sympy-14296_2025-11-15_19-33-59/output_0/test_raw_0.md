Here is the `reproducer.py` file that reproduces the issue:
```
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

def main():
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    correct_minpoly = sp.Poly(_x**2 + 2*_x - 1, _x, domain='QQ')
    try:
        assert sp.minimal_polynomial(a) == correct_minpoly
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script creates an algebraic number `b` and converts it to a `AlgebraicNumber` using `to_number_field`. It then checks if the minimal polynomial of `a` is correct. If not, it raises an `AssertionError`, prints the stack trace, and exits with code 1. If the issue is fixed, the script will exit with code 0.

You can run this script by executing `python3 reproducer.py` in the root directory of the project.