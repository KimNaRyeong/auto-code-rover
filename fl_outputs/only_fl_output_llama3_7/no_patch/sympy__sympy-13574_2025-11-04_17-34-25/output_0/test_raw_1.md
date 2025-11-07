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
    for percent in [1, 50, 99]:
        try:
            matrix = randMatrix(3, symmetric=True, percent=percent)
            if not is_symmetric(matrix):
                raise AssertionError("randMatrix did not generate a symmetric sparse matrix")
        except Exception as e:
            print_stacktrace(e)
            exit(1)

def is_symmetric(matrix):
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            if isinstance(matrix[i][j], sympy.Integer) and matrix[i][j] != matrix[j][i]:
                return False
    return True

if __name__ == "__main__":
    reproduce_issue()
```

This script will run `randMatrix` with different percentages and check if the generated matrix is symmetric. If it's not, it will print the stack trace of the exception and exit with code 1.