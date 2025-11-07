Here is the reproducer script:

```python
import sympy as sp
from unittest import main

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
    sp.degree((sp.Symbol('x')-2)/(sp.sympify('x**2+1')), sp.Symbol('x'))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")

print("Issue reproduced successfully")
exit(0)
```

This script will attempt to compute the degree of a rational function using SymPy. If the issue is present, it will catch the exception and print the stack trace before raising an `AssertionError`.