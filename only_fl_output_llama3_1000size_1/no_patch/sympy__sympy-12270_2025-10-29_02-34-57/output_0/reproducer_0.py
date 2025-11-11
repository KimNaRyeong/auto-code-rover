import sympy as sp
from sympy import Mul, I

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

def reproduce_bug():
    x, y = sp.symbols('x y')
    expr1 = -2*x - 4*y - 8
    expr2 = (-2*x - 4*y - 8).extract_multiplicatively(-2)
    
    if not isinstance(expr2, (int, complex)):
        raise AssertionError("Expected an integer or complex number")
    print_stacktrace(Exception("Bug found"))

if __name__ == "__main__":
    reproduce_bug()
