import sympy as sp
from sympy import Rational, Mul

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
    x = sp.symbols('x')
    y = sp.symbols('y')

    try:
        result1 = Mul(Rational(1, 2), x + y, evaluate=False)
        result2 = Mul(x + y, Rational(1, 2), evaluate=False)
        
        if not (str(result1) == 'x + y\n───\n  2' and str(result2).startswith('x + y')):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
