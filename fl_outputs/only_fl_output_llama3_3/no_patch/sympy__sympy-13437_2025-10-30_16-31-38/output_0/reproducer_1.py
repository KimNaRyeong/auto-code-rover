import sympy as sp
from sympy import symbols, oo
import sys
import traceback

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
    try:
        n = symbols('n')
        result = sp.bell(n).limit(n, oo)
        assert str(result) == 'oo', "bell(n).limit(n, oo) should be oo"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue reproduced successfully")
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
