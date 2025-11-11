Here is the reproducer script:

```python
import sympy as sy
from io import StringIO
import traceback
import sys

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
        M1 = sy.Matrix.zeros(0, 0)
        M2 = sy.Matrix.zeros(0, 1)
        M3 = sy.Matrix.zeros(0, 2)
        M4 = sy.Matrix.zeros(0, 3)
        result = sy.Matrix.hstack(M1, M2, M3, M4).shape
        if result != (0, 6):
            raise AssertionError("Expected shape (0, 6) but got {}".format(result))
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    try:
        M1 = sy.Matrix.zeros(1, 0)
        M2 = sy.Matrix.zeros(1, 1)
        M3 = sy.Matrix.zeros(1, 2)
        M4 = sy.Matrix.zeros(1, 3)
        result = sy.Matrix.vstack(M1, M2, M3, M4).shape
        if result != (4, 3):
            raise AssertionError("Expected shape (4, 3) but got {}".format(result))
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

reproduce_issue()
```

This script will run the original code and check if the expected output is obtained. If not, it will print the stack trace of the exception and exit with a non-zero status code.