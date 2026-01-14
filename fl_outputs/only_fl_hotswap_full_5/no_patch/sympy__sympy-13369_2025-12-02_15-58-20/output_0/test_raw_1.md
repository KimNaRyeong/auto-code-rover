 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import *
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = Symbol('x')
M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])

try:
    M.eigenvals()
except MatrixError as e:
    print_stacktrace(e)
    assert False, "MatrixError should not be raised"

lam = Symbol('lambda')
eigenvals = solve(det(lam*eye(3) - M), lam)

if not eigenvals:
    raise AssertionError("Expected non-empty list of eigenvalues")
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    assert False, "MatrixError should not be raised"
AssertionError: MatrixError should not be raised
```
This indicates that the `MatrixError` was raised when calling `M.eigenvals()`, which is the issue being reproduced.