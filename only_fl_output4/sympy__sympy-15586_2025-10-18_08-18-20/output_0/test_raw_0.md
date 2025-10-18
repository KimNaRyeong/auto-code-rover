```python
# reproducer.py

import numpy as np
from sympy import *
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
    try:
        init_printing()

        X0 = MatrixSymbol('X0', 2, 2)
        xx = np.random.rand(4, 4) 
        # xx = np.random.randint(10, size=(4, 4)) # Uncommenting this line should make the code workable

        X0Inv = X0**-1
        np.linalg.inv(xx)  # This works fine, confirming `xx` is invertible with numpy

        symInv = lambdify(X0, X0Inv, 'numpy')  # Enforcing numpy module for lambdify
        result = symInv(xx)  # The problematic line

        assert not isinstance(result, Exception), "Inversion failed"

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue with matrix inversion using sympy and numpy") from e

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the given issue where lambdify fails with a TypeError when trying to perform matrix inversion with sympy and numpy. It uses the indicated stack-tracing function to provide clearer error messages and context. When the issue is present, the script will raise an `AssertionError` and print a stack trace of the triggering exception.

For clarity, I've also enforced the use of numpy within `lambdify` by passing `'numpy'` as the module parameter, although in the provided code snippet, this parameter is not specified which could be a part of the issue — lambdify might not default to using numpy for operations, resulting in the TypeError. However, in this reproducible script, the aim is mainly to capture and report the type of exception as given in the original issue description.