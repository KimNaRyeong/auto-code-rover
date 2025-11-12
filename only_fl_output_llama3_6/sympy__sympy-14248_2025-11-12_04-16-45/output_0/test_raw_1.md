Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, pprint, latex
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

try:
    A = sp.MatrixSymbol('A', 2, 2)
    B = sp.MatrixSymbol('B', 2, 2)
    assert str(A - A*B - B) == "-B + -A⋅B + A"
    assert repr(A - A*B - B) == "Matrix(-1*B + -A*B + A)"
    assert latex(A - A*B - B) == r"-{\mathbf{B}} + {-}\mathbf{{A}}\cdot{\mathbf{B}} + \mathbf{{A}}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace with line numbers. If the issue is fixed, it will simply exit with code 0.