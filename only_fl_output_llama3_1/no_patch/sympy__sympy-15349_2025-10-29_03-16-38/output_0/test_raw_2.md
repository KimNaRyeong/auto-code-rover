Here is the reproducer script:

```python
import sympy
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

try:
    import sympy
    from sympy import *
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    result = trigsimp(q.to_rotation_matrix())
    
    if not all([result[i][1].is_Sin() and result[i][1].as_simplify().args[1] < 0 for i in range(3)]):
        raise AssertionError("Incorrect result with Quaternion.to_rotation_matrix()")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed.")
exit(0)
```

This script will attempt to reproduce the issue by creating a quaternion and converting it to a rotation matrix. If the resulting matrix does not have the expected form (i.e., one of the `sin(x)` terms is negative), an `AssertionError` will be raised, which will trigger the print_stacktrace function to print the stack trace of the error.