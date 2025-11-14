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

try:
    M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
    X = sp.MatrixSymbol('X', 1, 2)
    pdf = density(M)(X).doit()
    
    # The actual PDF should be:
    expected_pdf = "something"  # Replace with the correct expected PDF
    
    assert str(pdf) == expected_pdf, "PDF does not match the expected result"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
