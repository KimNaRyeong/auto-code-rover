import sympy as sp
from sympy.stats import density, MatrixNormal
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
    M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
    X = sp.MatrixSymbol('X', 1, 2)
    pdf = density(M)(X).doit()
    
    expected_pdf = 'exp(-tr(X.T*Matrix([[1, 0], [0, 1]])*X + Matrix([[-1, -2]]))*Matrix([[-1, -2]]).T/2)/(2*pi)'
    
    try:
        assert str(pdf) == expected_pdf
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
