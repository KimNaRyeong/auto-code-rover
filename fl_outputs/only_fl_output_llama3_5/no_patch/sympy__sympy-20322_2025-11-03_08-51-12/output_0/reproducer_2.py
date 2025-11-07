import sympy
from sympy import ceiling, simplify

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

def reproduce_issue():
    expected = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
    actual = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()
    if expected != actual:
        raise AssertionError("Inconsistent behavior for sympify/simplify with ceiling")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)

