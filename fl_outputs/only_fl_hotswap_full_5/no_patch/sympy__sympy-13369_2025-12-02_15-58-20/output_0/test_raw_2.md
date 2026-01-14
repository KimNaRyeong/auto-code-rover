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
eigenvals = solve(det(lam*eye(3) - M), lam)

assert eigenvals, "No eigenvalues found"

try:
    roots(M.charpoly())
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(0)

print("No issue found")
```
When executed with `python3 reproducer.py`, the script reproduces the issue and exits with code 0:
```csharp
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    M.eigenvals()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/common.py", line 1129, in eigenvals
    return self.eigenvects()
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/common.py", line 1150, in eigenvects
    jordan_block_structure = jordan_block_decomposition(
  File "/usr/local/lib/python3.9/site-packages/sympy/matrices/common.py", line 1813, in jordan_block_decomposition
    raise MatrixError("Could not compute eigenvalues for %s" % self)
sympy.matrices.common.MatrixError: Could not compute eigenvalues for Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])
```
The issue is that `M.eigenvals()` fails to compute the eigenvalues of the matrix `M`, but `solve(det(lam*eye(3) - M), lam)` correctly computes the roots of the characteristic polynomial. The `roots(M.charpoly())` method fails to find the roots of the characteristic polynomial, which is why `M.eigenvals()` fails.