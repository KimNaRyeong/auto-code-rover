import sys
import traceback
from sympy import sympify, ceiling, simplify

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    x = 0
    expr1 = sympify('4*ceiling(x/4 - 3/4)', evaluate=False)
    expr2 = sympify('4*ceiling(x/4 - 3/4)', evaluate=True)

    if expr1.simplify() != expr2.simplify():
        raise AssertionError("Inconsistent behavior for sympify/simplify with ceiling")

if __name__ == "__main__":
    try:
        reproduce_issue()
        print("The issue is fixed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
