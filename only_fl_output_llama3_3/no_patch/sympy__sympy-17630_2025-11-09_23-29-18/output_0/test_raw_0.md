Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, ZeroMatrix, BlockMatrix

def block_collapse(b):
    return b * b * b

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
    a = sp.MatrixSymbol("a", 2, 2)
    z = ZeroMatrix(2, 2)
    b = BlockMatrix([[a, z], [z, z]])
    
    try:
        block_collapse(b)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script defines the `reproduce_issue` function that creates a BlockMatrix with zero blocks and then attempts to multiply it three times using the `block_collapse` function. If an exception is raised, it prints the stack trace and raises an AssertionError.