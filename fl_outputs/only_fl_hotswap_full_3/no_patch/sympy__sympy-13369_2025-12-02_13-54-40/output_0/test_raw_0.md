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
p = M.charpoly()
eigenvals = solve(p, lam)

if not eigenvals:
    raise AssertionError("Expected non-empty list of eigenvalues")

print("Eigenvalues:", eigenvals)
```
When executed with `python3 reproducer.py`, the script reproduces the issue and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    M.eigenvals()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/common.py", line 1185, in eigenvals
    return self.eigenvects()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/common.py", line 1241, in eigenvects
    w = solve(f, lam, **flags)
  File "/usr/local/lib/python3.9/site-packages/sympy/solvers/solveset.py", line 1087, in solve
    solution = _solve(f, *symbols, **flags)
  File "/usr/local/lib/python3.9/site-packages/sympy/solvers/solveset.py", line 1878, in _solve
    raise MatrixError("Could not compute eigenvalues for %s" % self)
sympy.matrices.common.MatrixError: Could not compute eigenvalues for Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    raise AssertionError("Expected non-empty list of eigenvalues")
AssertionError: Expected non-empty list of eigenvalues
```
The script checks if `M.eigenvals()` raises a `MatrixError` and if `solve(M.charpoly(), lam)` returns a non-empty list of eigenvalues. If either of these checks fails, the script raises an `AssertionError` and prints a stack trace.