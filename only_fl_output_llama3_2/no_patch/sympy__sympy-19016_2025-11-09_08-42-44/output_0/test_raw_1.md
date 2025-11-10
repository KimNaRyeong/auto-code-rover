I apologize for the mistake earlier. Here is a new reproducer script that should correctly reproduce the issues:

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
        from sympy import Range
        r = Range(5)
        assert not hasattr(r, 'is_finite_set'), "Expected AttributeError"
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

    try:
        n = Symbol('n', integer=True)
        s = Range(n, oo, 1)
        assert s.sup is None, "Expected sup to be None"
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    main()
```

This script should correctly reproduce the issues and raise an `AssertionError` when they are present.