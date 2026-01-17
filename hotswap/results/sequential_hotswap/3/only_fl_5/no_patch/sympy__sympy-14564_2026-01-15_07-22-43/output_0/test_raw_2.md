```python
import sympy as sp
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x, y = sp.symbols('x y')
    pi = sp.pi

    # Demonstrating ConditionSet usage and potential issues.

    # Test 1: Expected to be S.EmptySet after substitution out of interval.
    c = sp.ConditionSet(x, x > 5, sp.Interval(1, 7))
    try:
        result = c.subs(x,8)
        assert result != sp.Interval(1, 7), "Test 1 Failed: Substitution outside of interval did not return expected result."
    except AssertionError as e:
        print_stacktrace(e)

    # Test 2: Expected to return S.EmptySet for non-integer and out of condition.
    c = sp.ConditionSet(x, x > 5, sp.S.Integers)
    try:
        result = c.subs(x,2*pi)
        assert result != sp.S.Integers, "Test 2 Failed: Substitution with non-integer did not return expected result."
    except AssertionError as e:
        print_stacktrace(e)

    # Test 3: ConditionSet misled by condition unrelated to variable, substituting x in a condition dependent on x, while defining set with y.
    c = sp.ConditionSet(y, x > 5, sp.S.Integers)
    try:
        result_when_false = c.subs(x,4)
        result_when_true = c.subs(x,6)
        assert result_when_false == sp.S.EmptySet and result_when_true == sp.S.Integers, "Test 3 Failed: Substitution does not correctly apply the condition."
    except AssertionError as e:
        print_stacktrace(e)

    # TypeError Tests: Demonstrating the TypeError arising from checking membership in a way not logically consistent.
    try:
        _ = 6 in c
        _ = 3 in c
    except TypeError as e:
        print_stacktrace(e)

    # Automatic evaluation test: Exploring the should-be behavior of ConditionSet auto-evaluation.
    c = sp.ConditionSet(x, x > 5, sp.Interval(1, 3))
    try:
        assert c != sp.S.EmptySet, "Test 4 Failed: Autoevaluation to EmptySet not expected with logically possible condition."
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issues as described, with clear commentation on the intention behind each test block. The tests explore the functionality and possible problems within `ConditionSet` implementation, particularly focusing on its behavior with conditions, substituting values that are outside of the defined set or unrelated to the condition, and how the `ConditionSet` evaluates or should evaluate in these contexts. The script will raise `AssertionError` to indicate when an outcome does not match the expected behavior, providing insight into how the `ConditionSet` class might need modifications or improvements.