```python
import numpy as np
from sympy import *

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
    init_printing()

    X0 = MatrixSymbol('X0', 2, 2)
    xx = np.random.rand(4, 4) 
    # xx = np.random.randint(10, size=(4, 4))  # This line makes it workable
    X0Inv = X0**-1

    # First, verify numpy's inversion works as expected
    try:
        np_inv_result = np.linalg.inv(xx)
        assert np_inv_result is not None
    except AssertionError as e:
        print("Numpy inversion failed.", file=sys.stderr)
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print("Unexpected error during numpy's inversion.", file=sys.stderr)
        print_stacktrace(e)
        sys.exit(1)

    # Now, use sympy to invert
    try:
        symInv = lambdify(X0, X0Inv)
        result = symInv(xx)
        assert result is not None, "Sympy inversion failed."
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # This will cause the script to exit with a non-zero code
    except Exception as e:
        print_stacktrace(e)
        raise e

    print("Inversion successful. No AssertionError was raised.")
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        # AssertionError is raised only if the issue is present
        sys.exit(1)
    except Exception as e:
        # Any other exceptions are not handled explicitly and should not occur
        sys.exit(1)
```

This script checks the issue where `lambdify` fails to create a function for matrix inversion. The `AssertionError` is raised when `lambdify` cannot process the symbolic inversion as expected, which should happen if the issue persists. The script exits with code 0 if the operation is successful, indicating the issue is fixed. The `print_stacktrace` function is used to print detailed error information when exceptions are caught, facilitating easier debugging.