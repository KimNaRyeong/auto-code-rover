import sympy as sp
from sympy import Add, MatAdd, Symbol, MatrixSymbol
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

def reproduce_issue():
    x = Symbol('x')
    assert Add(x, x, evaluate=True) == 2*x
    assert Add(x, x, evaluate=False) == x + x

    A = MatrixSymbol('A', 2,2)
    assert MatAdd(A, A).doit() == 2*A
    try:
        if MatAdd(A, A, evaluate=True) != 2*A:
            raise AssertionError("MatAdd(A, A, evaluate=True) does not canonicalize the object")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
