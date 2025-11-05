Here is the reproducer script:

```python
import sympy
from sympy.matrices import randMatrix
import sys
import traceback

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

def is_symmetric(matrix):
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

try:
    print("Testing randMatrix with symmetric=True and percent=50")
    matrix = sympy.randMatrix(3, symmetric=True, percent=50)
    assert is_symmetric(matrix), "Symmetry failed"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Test passed")

sys.exit(0)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue.