Here is the reproducer script:

```python
import sympy as sy
from io import StringIO

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    error_file = StringIO()
    print("Traceback (most recent call last):", file=error_file)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=error_file)
        print(f"    {line_number}: {code_context}", file=error_file)
    error_message = f"{e.__class__.__name__}: {e}"
    print(error_message, file=error_file)
    error_file.seek(0)
    sys.stderr.write(error_file.read())
    sys.exit(1)

def reproduce_issue():
    try:
        M1 = sy.Matrix.zeros(0, 0)
        M2 = sy.Matrix.zeros(0, 1)
        M3 = sy.Matrix.zeros(0, 2)
        M4 = sy.Matrix.zeros(0, 3)
        expected_shape = (0, 6)
        actual_shape = sy.Matrix.hstack(M1, M2, M3, M4).shape
        if actual_shape != expected_shape:
            raise AssertionError("Matrix hstack behavior changed in sympy 1.1")
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == '__main__':
    reproduce_issue()
```

This script creates matrices with different shapes and checks if the expected shape is returned by `sy.Matrix.hstack`. If the actual shape does not match the expected shape, it raises an `AssertionError` with a stack trace.