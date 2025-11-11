Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import numpy as np
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

init_printing()

X0 = MatrixSymbol('X0',2,2)
xx = np.random.rand(4,4) 
X0Inv = X0**-1
np.linalg.inv(xx)
symInv = lambdify(X0,X0Inv)

try:
    symInv(xx)
except TypeError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
```
This script will reproduce the issue and raise an `AssertionError` with a stack trace when the issue is present. If the issue is fixed, it will exit with code 0 and print "Issue is fixed".