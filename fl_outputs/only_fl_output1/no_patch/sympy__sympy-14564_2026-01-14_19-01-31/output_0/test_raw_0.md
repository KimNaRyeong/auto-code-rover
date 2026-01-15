```python
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
    from sympy import symbols, Interval, pi, S
    from sympy.sets.conditionset import ConditionSet
    x, y = symbols('x y')

    # Test 1: Check if ConditionSet correctly represents its definition
    try:
        c = ConditionSet(x, x > 5, Interval(1, 7))
        assert not 8 in c, "8 should not be in the condition set"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # Test 2: Check substitution behavior
    try:
        c = ConditionSet(x, x > 5, Interval(1, 7))
        result = c.subs(x, 8)
        assert result == S.EmptySet, "`subs` method did not return EmptySet"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # Test 3: Incorrect variable substitution handling
    try:
        c = ConditionSet(y, x > 5, S.Integers)
        result = c.subs(x, 6)
        assert result != S.Integers, "`subs` incorrect variable should not affect the set"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # Test 4: Autoevaluation check
    try:
        c = ConditionSet(x, x > 5, Interval(1, 3))
        assert c != ConditionSet(x, x > 5, Interval(1, 3)), "ConditionSet should auto-evaluate to EmptySet"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    print("All tests passed.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        # Do not exit with error code 0 on AssertionError
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
```

This script is designed to assert the core issues identified with the `ConditionSet` usage and behavior in SymPy as described. It employs assertions to check whether the behavior matches expected outcomes and raises an `AssertionError` with a stack trace if the behavior is contrary to expectations. Note that adjustments may be needed based on future library updates or fixes.