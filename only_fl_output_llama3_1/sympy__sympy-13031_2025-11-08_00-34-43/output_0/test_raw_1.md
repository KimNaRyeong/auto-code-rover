Here is the reproducer script:

```python
import sympy as sy
from io import StringIO
from contextlib import redirect_stdout

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
            raise AssertionError("Matrix hstack changed in sympy 1.1")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def reproduce_issue_2():
    try:
        M1 = sy.Matrix.zeros(1, 0)
        M2 = sy.Matrix.zeros(1, 1)
        M3 = sy.Matrix.zeros(1, 2)
        M4 = sy.Matrix.zeros(1, 3)
        result = sy.Matrix.hstack(M1, M2, M3, M4).shape
        if result != (1, 6):
            raise AssertionError("Matrix hstack changed in sympy 1.1")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    reproduce_issue()
    reproduce_issue_2()
```

You can run this script using `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.