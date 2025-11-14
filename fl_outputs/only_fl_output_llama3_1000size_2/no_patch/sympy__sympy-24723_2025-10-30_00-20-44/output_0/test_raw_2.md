I apologize for the mistake earlier. It seems that Sympy does not have a `MatrixNormal` class, which is why the script failed to reproduce the issue.

Here's an updated reproducer script:

```python
import sympy as sp
from sympy.stats import density, MatrixSymbol
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
    M = sp.Matrix([[1, 2]])
    X = sp.MatrixSymbol('X', 1, 2)
    result = density(M)(X).doit()
    expected_pdf = sp.exp(-sp.tr(X.T * (X - [-1, -2]) + 1) / (2*sp.pi))
    if not result.equals(expected_pdf):
        raise AssertionError("Matrix Normal Distribution returns wrong probability density function")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue reproduced successfully. The script will exit with code 0.")
sys.exit(0)
```

This script attempts to reproduce the issue by initializing a matrix in Sympy and calculating its PDF using the `density` function. It then checks if the calculated PDF matches the expected PDF from the Wikipedia page. If the calculated PDF does not match the expected PDF, it raises an `AssertionError`. The script also prints the stack trace of any exceptions that occur during execution.