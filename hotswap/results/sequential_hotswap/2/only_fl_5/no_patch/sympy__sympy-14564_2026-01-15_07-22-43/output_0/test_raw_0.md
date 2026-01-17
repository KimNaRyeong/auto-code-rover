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

def test_conditionset_behavior():
    x, y = sp.symbols('x y')
    pi = sp.pi

    # Test 1
    c = sp.ConditionSet(x, x > 5, sp.Interval(1, 7))
    try:
        assert c.subs(x, 8) is sp.S.EmptySet, "Expected EmptySet after substitution with a value out of range"
    except AssertionError as e:
        print_stacktrace(e)

    # Test 2
    c = sp.ConditionSet(x, x > 5, sp.S.Integers)
    try:
        assert c.subs(x, 2 * pi) is sp.S.EmptySet, "Expected EmptySet after substitution with a value not in Integers"
    except AssertionError as e:
        print_stacktrace(e)

    # Test 3
    c = sp.ConditionSet(y, x > 5, sp.S.Integers)
    try:
        result = c.subs(x, 4)
        assert result is sp.S.EmptySet, "Expected EmptySet when condition is False"
        result = c.subs(x, 6)
        assert result == sp.S.Integers, "Expected S.Integers when condition is True"
    except AssertionError as e:
        print_stacktrace(e)

    # Test 4
    try:
        assert 6 not in c, "Expected 6 not to be in ConditionSet with condition x > 5"
    except TypeError as e:
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)

    # Test 5
    try:
        assert 3 not in c, "Expected 3 not to be in ConditionSet with condition x > 5"
    except TypeError as e:
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)

    # Test for autoevaluation
    c = sp.ConditionSet(x, x > 5, sp.Interval(1, 3))
    try:
        assert c == sp.S.EmptySet, "Expected ConditionSet to autoevaluate to EmptySet when condition cannot be met"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_conditionset_behavior()
    sys.exit(0)
```