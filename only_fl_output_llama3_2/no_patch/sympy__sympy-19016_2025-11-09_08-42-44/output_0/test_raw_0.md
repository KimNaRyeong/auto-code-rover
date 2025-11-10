Here is the reproducer script for both issues:

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

def main():
    try:
        n = Symbol('n', integer=True)
        s = Range(n, oo, 1)
        s.sup
    except ValueError as e:
        print_stacktrace(e)
        assert False, "Expected ValueError"

    try:
        from sympy import Range
        Range(5).is_finite_set
    except AttributeError as e:
        print_stacktrace(e)
        assert False, "Expected AttributeError"

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issues are present and print a stack trace of the issue.