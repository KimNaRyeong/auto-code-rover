 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import MatrixSymbol, tr, exp, pi, Matrix
from sympy.stats import density, MatrixNormal

def print_stacktrace(e: Exception):
    import traceback    import sys
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
    actual_pdf = density(M)(X).doit()
    expected_pdf = (-tr(Matrix([[-1, -2]]) + X.T * X) / 2).exp() / (2 * pi)
    assert actual_pdf == expected_pdf, "The PDFs are not equal"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements. The difference is in the constant of the PDF, as explained in the issue.