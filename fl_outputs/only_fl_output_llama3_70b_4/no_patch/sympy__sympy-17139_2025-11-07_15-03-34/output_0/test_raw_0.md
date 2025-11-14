Here is the `reproducer.py` file that reproduces the issue:
```
import sympy
from sympy import Symbol, I

def reproduce_issue():
    x = Symbol('x')
    try:
        result = sympy.simplify(sympy.cos(x)**I)
        assert False, "Expected TypeError, but no exception was raised"
    except TypeError as e:
        print_stacktrace(e)

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

if __name__ == "__main__":
    reproduce_issue()
```
This script will raise an `AssertionError` if the issue is fixed, and print a stack trace of the `TypeError` exception when the issue is present.