Here is the reproducer script:

```python
import sympy as sp
from sympy import Mul, I, x, y

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
    (2*x + 4*y + 8).extract_multiplicatively(-2)
except Exception as e:
    print_stacktrace(e)
    raise
```

This script will attempt to extract multiplicatively `-2` from `(2*x + 4*y + 8)`. If the issue is present, it will catch the exception and print a stack trace.