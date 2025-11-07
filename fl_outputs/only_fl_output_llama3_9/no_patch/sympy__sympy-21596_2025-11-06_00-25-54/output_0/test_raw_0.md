Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import I, n

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
    S1 = sp.imageset(lambda n: n + (n - 1)*(n + 1)*I, sp.S.Integers)
    assert not (2 in S1), "Expected 2 not to be in S1"
    assert not (2 in S1.intersect(sp.Reals)), "Expected 2 not to be in S1 intersect Reals"

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully. Exiting with code 0.")
exit(0)
```

This script reproduces the issue by creating an image set `S1` and checking if `2` is in `S1` and also in the intersection of `S1` and the real numbers. If the assertions fail, it prints a stack trace and exits with code 1. Otherwise, it prints a success message and exits with code 0.