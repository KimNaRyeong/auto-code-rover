Here is the reproducer script:

```python
import sympy as sp
from sympy import symbols, Interval, S
from sympy.sets.conditionset import ConditionSet

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
    x = symbols('x')
    c = ConditionSet(x, x > 5, Interval(1, 7))
    try:
        assert c.subs(x, 8) == S.EmptySet()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def main():
    reproduce_issue()

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. It will also exit with code 0 when the issue is fixed.