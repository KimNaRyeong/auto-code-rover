Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
from sympy import *
import traceback
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
    eigenvalues = M.eigenvals()
    assert len(eigenvalues) > 0
    lam = Symbol('lambda')
    char_poly = det(lam*eye(3) - M)
    roots = solve(char_poly, lam)
    assert len(roots) == 3
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

Please note that I added an additional assertion to check if the roots of the characteristic polynomial are correctly computed, which should be the case according to your description.