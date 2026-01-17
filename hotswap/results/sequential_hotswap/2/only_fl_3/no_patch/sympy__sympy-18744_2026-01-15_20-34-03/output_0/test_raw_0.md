```python
# reproducer.py
from sympy import MatrixSymbol, I
from sympy.core.compatibility import as_int

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

def test_imaginary_matrix_symbol():
    try:
        M = MatrixSymbol('M', 2, 2)
        expr = I*M
        str(expr)  # This is where the problem occurs
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("The issue with multiplying a MatrixSymbol by I is present.") from e

if __name__ == "__main__":
    test_imaginary_matrix_symbol()
    print("The issue is fixed. Exiting with code 0.")
```