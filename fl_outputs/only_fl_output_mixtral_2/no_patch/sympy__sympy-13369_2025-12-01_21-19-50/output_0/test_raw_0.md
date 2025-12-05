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
    eigenvals = M.eigenvals()
except MatrixError as e:
    print_stacktrace(e)
    assert False, "MatrixError should not be raised here"

try:
    charpoly = M.charpoly()
except NotImplementedError as e:
    print_stacktrace(e)
    assert False, "NotImplementedError should not be raised here"

roots = list(roots(charpoly))
if not roots:
    assert False, "roots(M.charpoly()) should return three roots of the characteristic polynomial"
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace of the issue. The script should also exit with code 1.

The script first defines the `print_stacktrace` function to print the stack trace of an exception. It then defines the symbol `x` and the matrix `M` as in the original issue.

The script then tries to compute the eigenvalues of `M` using the `eigenvals` method. If a `MatrixError` is raised, the script prints the stack trace and raises an `AssertionError`.

The script then tries to compute the characteristic polynomial of `M` using the `charpoly` method. If a `NotImplementedError` is raised, the script prints the stack trace and raises an `AssertionError`.

Finally, the script computes the roots of the characteristic polynomial using the `roots` function. If the roots are empty, the script raises an `AssertionError`.

The script should exit with code 1 to indicate that the issue is present.