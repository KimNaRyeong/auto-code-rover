Here is the reproducer script:

```python
import sympy as sm
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

try:
    M = sm.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
    V = sm.Matrix([[2], [2], [2], [2], [2], [2]])
    result = M.col_insert(3, V)
    if not str(result) == "Matrix([[1, 0, 0, 2, 2, 0, 0],\n       [0, 1, 0, 2, 2, 0, 0],\n       [0, 0, 1, 2, 2, 0, 0],\n       [0, 0, 0, 2, 2, 0, 0],\n       [0, 0, 0, 2, 2, 0, 0],\n       [0, 0, 0, 2, 2, 1, 0]])":
        raise AssertionError("Matrix col_insert() does not work correctly")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.