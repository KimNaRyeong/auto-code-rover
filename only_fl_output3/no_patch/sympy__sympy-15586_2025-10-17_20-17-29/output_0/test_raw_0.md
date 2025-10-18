```python
import numpy as np
from sympy import MatrixSymbol, lambdify
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    X0 = MatrixSymbol('X0', 2, 2)
    xx = np.random.rand(4,4)  # Example input matrix
    # Attempt to invert matrix using lambdify
    X0Inv = X0**-1
    try:
        # Calculate the inverse using numpy directly
        numpy_inv = np.linalg.inv(xx)
        print("Matrix inversion using Numpy works fine.")
        # Now attempt to calculate the inverse using sympy and lambdify
        symInv = lambdify(X0, X0Inv, modules=["numpy"])
        result = symInv(xx)
        # If the following line is reached, it means no exception was raised
        print("Matrix inversion using Sympy and Numpy (via lambdify) works fine.")
        sys.exit(0)  # Normal exit

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Matrix inversion using lambdify failed.") from e

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue described where matrix inversion using `sympy` and `numpy` via `lambdify` fails. The script should exit without errors when the issue is fixed, and if the issue is present, it will raise an `AssertionError` and print the corresponding stack trace to help track down the problem.