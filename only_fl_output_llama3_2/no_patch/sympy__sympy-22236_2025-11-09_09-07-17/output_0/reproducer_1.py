import sympy as sp
from io import StringIO
import sys
import traceback

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
    x, y = sp.symbols('x y')
    try:
        result1 = str(sp.Mul(sp.Rational(1, 2), x + y, evaluate=False))
        result2 = str(sp.Mul(x + y, sp.Rational(1, 2), evaluate=False))
        assert result1 == f"({str(x)} + {str(y)})/{2}"
        assert result2 == f"{str(x)} + {str(y)}*{1}/{2}"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
