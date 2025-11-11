Here is the standalone Python file `reproducer.py` to reproduce the issue:

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

def reproduce_issue():
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
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, execute `python3 reproducer.py` in your terminal. If the issue is present, it will print a stack trace and exit with code 1.