```python
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

def test_matrix_normal_pdf():
    from sympy import MatrixSymbol, symbols
    from sympy.stats import density, MatrixNormal
    import sympy as sp

    # Defining the matrix normal distribution
    M = MatrixNormal('M', sp.Matrix([[1, 2]]), sp.Matrix([[1]]), sp.Matrix([[1, 0], [0, 1]]))
    X = MatrixSymbol('X', 1, 2)

    # Expected PDF as mentioned in the correct formula on Wikipedia
    expected = sp.exp(-1/2 * (sp.trace((sp.Matrix([[1, 2]]).T + X) * (sp.Matrix([[-1, -2]]) + X)))) / (2 * sp.pi)

    # Actual PDF from sympy
    actual = density(M)(X).doit()

    # Assert equality, considering normalization
    assert sp.simplify(actual - expected) == 0, "The computed PDF does not match the expected one."

if __name__ == "__main__":
    try:
        test_matrix_normal_pdf()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    print("Test passed successfully.")
    SystemExit(0)
```