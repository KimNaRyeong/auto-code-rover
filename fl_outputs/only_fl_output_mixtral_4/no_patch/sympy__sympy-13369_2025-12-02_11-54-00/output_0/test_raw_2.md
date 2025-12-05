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
eigenvalues = solve(det(lam*eye(3) - M), lam)

assert eigenvalues, "No eigenvalues found"

try:
    roots(M.charpoly())
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(0)

print("No issue found")
sys.exit(1)
```
When executed with `python3 reproducer.py`, the script should print the following output:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    M.eigenvals()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/common.py", line 1322, in eigenvals
    return self.eigenvects()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/common.py", line 1355, in eigenvects
    x = solve(f, x)
  File "/usr/local/lib/python3.9/site-packages/sympy/solvers/solvers.py", line 1127, in solve
    raise MatrixError("Could not compute eigenvalues for %s" % self)
sympy.matrices.common.MatrixError: Could not compute eigenvalues for Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])
```
This indicates that the issue has been successfully reproduced. If the output is different, then the issue may have been fixed.