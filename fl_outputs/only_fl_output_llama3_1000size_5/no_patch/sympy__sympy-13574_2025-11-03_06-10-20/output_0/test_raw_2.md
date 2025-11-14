Here is the reproducer script:

```python
import sympy
from sympy.matrices import randMatrix, SparseMatrix

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
    for percent in [1, 50, 99]:
        matrix = randMatrix(3, symmetric=True, percent=percent)
        if not is_symmetric(matrix):
            raise AssertionError("randMatrix won't generate symmetric sparse matrices")
    print("Issue reproduced successfully")

def is_symmetric(matrix):
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```

This script will create a 3x3 symmetric sparse matrix with different percentages of non-zero elements and check if the generated matrix is indeed symmetric. If any of these matrices are not symmetric, it raises an `AssertionError` with the stack trace printed to stderr.