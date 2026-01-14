from sympy import Poly, S
from sympy.abc import x
import traceback
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

def main():
    # Multiplying an expression by a Poly does not evaluate when the expression is on the left side of the multiplication
    assert Poly(x)*x == x*Poly(x), "AssertionError: Multiplying an expression by a Poly should evaluate when the expression is on the left side of the multiplication"
    assert -2*Poly(x) == Poly(x)*S(-2), "AssertionError: Multiplying an expression by a Poly should evaluate when the expression is on the left side of the multiplication"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
