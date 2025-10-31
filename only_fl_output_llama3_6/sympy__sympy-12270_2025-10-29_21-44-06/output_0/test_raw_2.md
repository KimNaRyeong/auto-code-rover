Here is the reproducer script:

```python
import sympy as sp

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
    (2*sp.I).extract_multiplicatively(-2)
except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print_stacktrace(e)
    raise
```

This script will attempt to extract multiplicatively `-2` from `(2*I)`. If the issue is present, it will catch the exception and print a stack trace.