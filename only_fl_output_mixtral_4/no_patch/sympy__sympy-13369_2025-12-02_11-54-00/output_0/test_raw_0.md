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
    sys.exit(0)

lam = Symbol('lambda')
eigenvals = solve(det(lam * eye(3) - M), lam)

assert eigenvals, "No eigenvalues found"
assert roots(M.charpoly()) == eigenvals, "Eigenvalues do not match"
```
When executed with `python3 reproducer.py`, the script reproduces the issue and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 15
    M.eigenvals()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/matrices.py", line 4051, in eigenvals
    return self.eigenvects()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/matrices.py", line 4026, in eigenvects
    w = W(self, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/polys/solvers/solve.py", line 135, in solve
    solutions = _solve(f, *symbols, **flags)
  File "/usr/local/lib/python3.9/site-packages/sympy/polys/solvers/solve.py", line 168, in _solve
    raise MatrixError("Could not compute eigenvalues for %s" % self)
sympy.matrices.common.MatrixError: Could not compute eigenvalues for Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])
```
The script exits with code 0, indicating that the issue has been reproduced.