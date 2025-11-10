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
    Add(x, x, evaluate=True)  # This should work
    Add(x, x, evaluate=False)  # This should also work

    A = MatrixSymbol('A', 2,2)
    MatAdd(A, A)  # This should not be evaluated
    try:
        assert str(MatAdd(A, A, evaluate=True)) == "2*A"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
