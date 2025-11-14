Here is the reproducer script:

```python
import sympy
from sympy.matrices import randMatrix

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

def reproduce_issue():
    try:
        assert sympy.Matrix([[1, 2], [2, 3]]).is_symmetric
        matrix = randMatrix(3, symmetric=True, percent=50)
        if not matrix.is_symmetric:
            raise AssertionError("randMatrix did not generate a symmetric matrix")
        matrix = randMatrix(3, symmetric=True, percent=99)
        if not matrix.is_symmetric:
            raise AssertionError("randMatrix did not generate a symmetric matrix")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `randMatrix` function with different parameters and check if the resulting matrix is symmetric. If any of these checks fail, it will raise an `AssertionError`, print the stack trace, and exit with code 1.