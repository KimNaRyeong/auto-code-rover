Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import sympy as sp
from sympy import Interval, S

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

x, y = sp.symbols('x y')

try:
    c = ConditionSet(x, x > 5, Interval(1, 7))
    assert c.subs(x, 8) == S.EmptySet
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

try:
    c = ConditionSet(x, x > 5, S.Integers)
    assert c.subs(x, 2 * sp.pi) == S.Integers
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

try:
    c = ConditionSet(y, x > 5, S.Integers)
    assert (6 in c) == True
except TypeError as e:
    print_stacktrace(e)
    exit(1)

try:
    c = ConditionSet(x, x > 5, Interval(1, 3))
    assert c.doit() == False
except AttributeError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed")
exit(0)
```
This script will raise an `AssertionError` or a `TypeError` when the issue is present and print a stack trace of the issue. It will also exit with code 0 when the issue is fixed.