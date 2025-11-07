Here is the reproducer script:

```python
import sympy as sp
from sympy import symbols, tanh, csch, sech, csc, sec
import unittest
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    x, y = symbols('x y')
    try:
        from sympy.functions.elementary.trigonometric import expand_trig
        if expand_trig(csch(x + y)) != csch(x + y):
            raise AssertionError("Expected csch(x+y) but got something else")
        if expand_trig(sech(x + y)) != sech(x + y):
            raise AssertionError("Expected sech(x+y) but got something else")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    test_issue()
```

This script attempts to call `expand_trig` with `csch(x + y)` and `sech(x + y)` and checks if the result is equal to the original expression. If not, it raises an `AssertionError`.