Here is the reproducer script:

```python
import numpy as np
from sympy import *
init_printing()
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
    import numpy as np
    from sympy import *
    init_printing()
    
    X0 = MatrixSymbol('X0',2,2)
    xx = np.random.rand(4,4) 
    X0Inv = X0**-1
    np.linalg.inv(xx)
    symInv = lambdify(X0,X0Inv)
    symInv(xx)
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue should be reproducible"
else:
    print("Issue is fixed")
    exit(0)

```

This script tries to reproduce the issue by running the original code. If an exception occurs during execution (which it does), it prints the stack trace and asserts that the issue should still be present.