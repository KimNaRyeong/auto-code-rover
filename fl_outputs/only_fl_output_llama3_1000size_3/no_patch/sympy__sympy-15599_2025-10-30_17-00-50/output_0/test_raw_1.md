Here is the reproducer script:

```python
import sympy as sp

def reproduce_issue():
    from sympy.core.mod import Mod
    i = sp.symbols('i', integer=True)
    assert not (Mod(3*i, 2) == Mod(i, 2))

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue not present")
    exit(0)

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
```

This script reproduces the issue by asserting that `Mod(3*i, 2)` is not equal to `Mod(i, 2)`. If this assertion fails (i.e., the issue is present), it prints the stack trace and exits with code 1. Otherwise, it prints a message indicating that the issue is not present and exits with code 0.