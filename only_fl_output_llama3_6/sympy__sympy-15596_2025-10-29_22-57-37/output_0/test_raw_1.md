Here is the reproducer script:

```python
import sympy as sp
from sys import exit, stderr

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=stderr)
        print(f"    {line_number}: {code_context}", file=stderr)
    print(f"{e.__class__.__name__}: {e}", file=stderr)

try:
    f = sp.sympify("(x-2)/(x**2+1)")
    degree = sp.degree(f, "x")
    self = assert degree == 1
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace.