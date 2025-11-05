import sympy as sp
from sympy.stats import density, MatrixNormal
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
        from sympy import MatrixSymbol
        M = sp.stats.MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
        X = sp.MatrixSymbol('X', 1, 2)
        assert density(M)(X).doit() == "expected pdf value", f"Expected {density(M)(X).doit()} but got {density(M)(X).doit()}"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
