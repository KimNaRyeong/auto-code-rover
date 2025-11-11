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
        for percent in [1, 50, 99]:
            m = randMatrix(3, symmetric=True, percent=percent)
            if not m.is_symmetric:
                raise AssertionError("Symmetric matrix is expected")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will test the `randMatrix` function with different percentages (1, 50, and 99) to see if it generates symmetric matrices. If any of these tests fail, it will catch the exception and print the stack trace.