 Here is a standalone Python script `reproducer.py` that reproduces the issues:
```python
from sympy import ConditionSet, Interval, S, symbols
from sympy.sets.sets import Set

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols('x')

# Issue 1: ambiguous behavior of ConditionSet
c = ConditionSet(x, x > 5, Interval(1, 7))
assert c.subs(x, 8) == Interval(1, 7), "ConditionSet.subs should return the base set when the condition is not satisfied"
assert 8 in c is False, "8 should not be in c"

c = ConditionSet(x, x > 5, S.Integers)
assert c.subs(x, 2 * pi) == S.Integers, "ConditionSet.subs should return the base set when the condition is not satisfied"
assert (2 * pi) in c is False, "2*pi should not be in c"

c = ConditionSet(y, x > 5, S.Integers)
assert c.subs(x, 4) == Set.EmptySet, "ConditionSet.subs should return the empty set when the condition is not satisfied"
assert c.subs(x, 6) == S.Integers, "6 should be in c"

try:
    3 in c
except TypeError as e:
    print_stacktrace(e)

# Issue 2: should there be a doit method or autoevaluation for something like this?
c = ConditionSet(x, x > 5, Interval(1, 3))
assert str(c) != "ConditionSet(x, x > 5, Interval(1, 3))", "ConditionSet should evaluate to False"

# Issue 3: other fixes
c = ConditionSet(x, x > 5, Interval(1, 7))
assert c.subs(x, 8) == Set.EmptySet, "ConditionSet.subs should return the empty set when the condition is not satisfied"

c = ConditionSet(x, x > 5, Interval(1, 7))
dummy = symbols('n', negative=True)
assert c.subs(x, dummy) == ConditionSet(dummy, x > 5, Interval(1, 7)), "The dummy variable should not affect the condition"
```
The script defines the `print_stacktrace` function to print the stack trace and then defines the symbols and conditions to reproduce the issues. The script asserts that the behavior of `ConditionSet` is as expected, and if not, it raises an `AssertionError` with a stack trace.

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issues are fixed, the script should exit with code 0 without printing any error messages.