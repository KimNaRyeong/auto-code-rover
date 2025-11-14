Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
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

def main():
    M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
    X = sp.MatrixSymbol('X', 1, 2)
    pdf = density(M)(X).doit()

    expected_pdf = sp.exp(-sp.trace((X - sp.Matrix([[1], [2]])) * sp.Matrix([[1, 0], [0, 1]]) * (X - sp.Matrix([[1], [2]])).T) / 2) / sp.pi

    try:
        assert str(pdf) == str(expected_pdf)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script initializes a matrix normal distribution with the given parameters, computes the PDF using Sympy, and compares it to the expected PDF. If the two do not match, an `AssertionError` is raised, and the stack trace is printed using the provided function. The script exits with code 1 if the issue is present and code 0 if the issue is fixed.

Note that I've corrected the expected PDF formula to match the one in the Wikipedia page you mentioned.