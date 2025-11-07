Here is the `reproducer.py` file that reproduces the issue:

```python
import sympy as sp
from sympy.abc import x

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
    from sympy import degree
    assert degree((x-2)/(x**2+1), x) == 1, "Expected the degree of (x-2)/(x**2+1) to be 1"
except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print_stacktrace(e)
    raise
```

This script will first import the `degree` function from SymPy. Then, it will assert that the degree of `(x-2)/(x**2+1)` is 1. If this assertion fails, it will print a stack trace and raise an `AssertionError`.