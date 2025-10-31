Here is the reproducer script:

```python
import numpy as np
from sympy import *
init_printing()

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
    X0 = MatrixSymbol('X0',2,2)
    xx = np.random.rand(4,4) 
    X0Inv = X0**-1
    np.linalg.inv(xx)
    symInv = lambdify(X0,X0Inv)
    symInv(xx)
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue should be reproduced"
else:
    print("Issue not present")
    exit(0)
```

This script will attempt to reproduce the issue by running the code that is supposed to cause the error. If an exception is raised during this process, it will print a stack trace and then fail the assertion with the message "Issue should be reproduced".