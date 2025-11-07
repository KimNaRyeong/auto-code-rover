import sympy as sp
from sympy import MatrixSymbol
from sympy.stats import density, MatrixNormal

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

def main():
    M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
    X = MatrixSymbol('X', 1, 2)
    pdf = density(M)(X).doit()

    expected_pdf_str = r'exp(-tr(X.T*Matrix([[-1, -2]]) + X)/2)/(2*pi)'
    try:
        assert str(pdf) == expected_pdf_str
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
