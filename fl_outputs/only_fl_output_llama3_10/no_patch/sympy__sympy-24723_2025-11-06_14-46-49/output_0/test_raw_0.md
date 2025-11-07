Here is the reproducer script:

```python
import sympy as sp
from sympy.stats import density, MatrixNormal
import sys
import traceback

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
    from sympy import MatrixSymbol
    M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
    X = MatrixSymbol('X', 1, 2)
    density(M)(X).doit()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not reproduced. Everything looks good.")
sys.exit(0)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace of the error. If the issue is fixed, it will simply print a success message and exit with code 0.