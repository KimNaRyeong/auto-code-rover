Here is the `reproducer.py` file that reproduces the issue:
```
import numpy as np
from sympy import *
init_printing()

def reproduce_issue():
    X0 = MatrixSymbol('X0', 2, 2)
    xx = np.random.rand(4, 4) 
    X0Inv = X0**-1
    symInv = lambdify(X0, X0Inv)
    try:
        symInv(xx)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"

if __name__ == "__main__":
    reproduce_issue()
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

You can run this script using `python3 reproducer.py`.