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

def main():
    try:
        c = sp.ConditionSet(x, x > 5, sp.Interval(1, 7))
        assert not (8 in c)
    except Exception as e:
        print_stacktrace(e)
        raise

    try:
        c = sp.ConditionSet(y, x > 5, sp.Integers)
        assert c.subs(x, 4) == sp.EmptySet()
    except Exception as e:
        print_stacktrace(e)
        raise

    try:
        c = sp.ConditionSet(y, x > 5, sp.Integers)
        assert not (3 in c)
    except Exception as e:
        print_stacktrace(e)
        raise

    try:
        c = sp.ConditionSet(x, x > 5, sp.Interval(1, 3))
        assert c.doit() == sp.EmptySet()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will run the tests and if any of them fail, it will print the stack trace and raise an `AssertionError`.