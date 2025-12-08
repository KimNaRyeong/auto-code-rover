import sys
import traceback
from sympy import pprint, Symbol, DiracDelta

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = Symbol('x')
    try:
        pprint(x * DiracDelta(x, 1))
    except TypeError as e:
        print_stacktrace(e)
        assert False, "Issue present"

if __name__ == "__main__":
    main()
