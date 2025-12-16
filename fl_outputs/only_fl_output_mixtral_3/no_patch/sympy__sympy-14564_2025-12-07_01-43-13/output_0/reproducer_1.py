from sympy import ConditionSet, Interval, S, symbols
from sympy.sets.sets import Set
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

# Issue 2: should there be a doit method or autoevaluation for something like this?
c = ConditionSet(x, x > 5, Interval(1, 3))
# The following line should evaluate to False, but it doesn't
assert c == False, "ConditionSet should evaluate to False when the condition is not satisfied"

# Issue 3: other fixes
assert ConditionSet(x, x > 5, Interval(1, 7)).subs(x, 8) == Set.EmptySet
assert ConditionSet(x, x > 5, Interval(1, 7)).subs(x, symbols('n', negative=True)) == Interval(1, 3)
