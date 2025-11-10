Here is the reproducer script:

```python
import sympy as sp
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

def reproduce_issue():
    A1, A2 = symbols('A1,A2')
    f1 = Xor(A1, A2)
    f2 = ~(Xor(A1, A2))
    
    try:
        assert bool_map(f2, f1) != ((A1 & A2) | (~A1 & ~A2), {A1: A1, A2: A2}), "Expected different result"
        print(bool_map(f2, f1))
        print(bool_map(f1, f2))
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will execute the original code and check if the result of `bool_map(f2, f1)` is equal to `((A1 & A2) | (~A1 & ~A2), {A1: A1, A2: A2})`. If it's not equal, an `AssertionError` will be raised with a stack trace.