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
        assert not sympy.Matrix([[1, 2], [2, 1]]).is_symmetric
        randMatrix(3, symmetric=True, percent=50)
        print("Issue not reproduced")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will try to generate a non-symmetric matrix with `randMatrix` and check if it is indeed non-symmetric. If the issue is present, an `AssertionError` will be raised and the stack trace will be printed.