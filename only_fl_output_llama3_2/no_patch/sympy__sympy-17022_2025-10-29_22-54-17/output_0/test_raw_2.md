Here is the reproducer script:

```python
import sympy as sp
from sympy import symbols, MatrixSymbol, lambdify, eye, I
import numpy as np

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

def main():
    try:
        n = symbols('n', integer=True)
        A = MatrixSymbol("A", n, n)
        a = np.array([[1, 2], [3, 4]])
        f = lambdify(A, A + sp.eye(n))
        result = f(a)
        assert np.allclose(result, [[2, 2], [3, 5]]), "Issue not reproduced"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will attempt to reproduce the issue by creating a symbolic expression using SymPy's `lambdify` function. If the issue is present, it will print the stack trace and raise an assertion error.