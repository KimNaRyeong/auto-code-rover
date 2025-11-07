Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from sympy import Mul, I

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

def reproduce_bug():
    x, y = sp.symbols('x y')
    expr1 = -2*x - 4*y - 8
    expr2 = (-2*x - 4*y - 8).extract_multiplicatively(-2)
    
    try:
        assert expr2 == 1 + 2*I, "Multiplicatively extracting -2 from -2x-2y failed"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_bug()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If you run this script, it should output the expected error message along with the stack trace.