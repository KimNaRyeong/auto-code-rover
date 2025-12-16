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
    assert 6 in c
except TypeError as e:
    print_stacktrace(e)

try:
    3 in c
except TypeError as e:
    print_stacktrace(e)

# Issue 2: perhaps an error at instantiation should be raised if the condition is not a function of the given variable
try:
    ConditionSet(x, x**2 > 5, Interval(1, 3))
except ValueError as e:
    print_stacktrace(e)
else:
    raise AssertionError("ValueError should be raised when the condition is not a function of the given variable")

# Issue 3: should there be a doit method or autoevaluation for something like this?
c = ConditionSet(x, x > 5, Interval(1, 3))
assert c == ConditionSet(x, x > 5, Interval(1, 3)), "ConditionSet should not be evaluated to False"

# Issue 4: ConditionSet(x, x > 5, Interval(1, 7)).subs(x, 8) should be S.EmptySet
c = ConditionSet(x, x > 5, Interval(1, 7))
assert c.subs(x, 8) == Set.EmptySet, "ConditionSet.subs should return the empty set when the condition is not satisfied"

# Issue 5: ConditionSet(x, x > 5, Interval(1, 7)).subs(x, Symbol('n', negative=True)) should be unchanged
from sympy import Symbol
c = ConditionSet(x, x > 5, Interval(1, 7))
assert c.subs(x, Symbol('n', negative=True)) == c, "ConditionSet.subs should not change the set when the dummy variable is used"
```
The script defines the `print_stacktrace` function to print the stack trace of an exception, and then defines several `ConditionSet` objects to reproduce the issues. The script asserts that the behavior of the `ConditionSet` objects matches the expected behavior, and raises an `AssertionError` when the behavior is not as expected.

When the script is executed with `python3 reproducer.py`, it will print the stack trace of the `AssertionError` exceptions, which will show the line numbers of the statements that caused the issues. When the issues are fixed, the script will exit with code 0