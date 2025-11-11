Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x, y

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
    c = sp.ConditionSet(x, x > 5, sp.Interval(1, 7))
    try:
        assert c.subs(x, 8) == sp.EmptySet()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.