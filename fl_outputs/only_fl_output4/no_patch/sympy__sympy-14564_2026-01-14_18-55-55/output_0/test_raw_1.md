To create a Python script named `reproducer.py` that reproduces the outlined issues and utilizes the provided `print_stacktrace` function for clear error reporting, follow the template below. This script checks the behavior of `ConditionSet` in Sympy and asserts the expected behavior based on the initial issue description. Errors and mismatches are clearly reported using stack traces.

```python
import sympy as sp
from sympy import S, Interval

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

def test_conditions():
    x = sp.Symbol('x')
    pi = sp.pi

    # First scenario
    c = sp.ConditionSet(x, x > 5, Interval(1, 7))
    try:
        assert c.subs(x, 8) == S.EmptySet, "Substitution outside base set should result in EmptySet"
    except AssertionError as e:
        print_stacktrace(e)

    # Second scenario
    c = sp.ConditionSet(x, x > 5, S.Integers)
    try:
        assert c.subs(x, 2*pi) == S.Integers, "Condition does not alter base set on substitution"
    except AssertionError as e:
        print_stacktrace(e)

    # Third scenario
    y = sp.Symbol('y')
    c = sp.ConditionSet(y, x > 5, S.Integers)
    try:
        assert c.subs(x, 4) == S.EmptySet, "Unrelated substitution with false condition should yield EmptySet"
        assert c.subs(x, 6) == S.Integers, "Unrelated substitution with true condition should return base set"
    except AssertionError as e:
        print_stacktrace(e)

    # Fourth scenario: Testing 'in' behavior
    try:
        result = 6 in c
    except TypeError as e:
        print_stacktrace(e)
        result = False
    assert not result, "'in' operation with condition not depending on the set variable should not work"

    # Fifth scenario: Simplification/evaluation test
    c = sp.ConditionSet(x, x > 5, Interval(1,3))
    try:
        assert c == S.EmptySet, "ConditionSet with no possible matches should simplify to EmptySet"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_conditions()
```

This script systematically approaches each aspect of the issue you've raised with `ConditionSet` in Sympy. By using assertions, it tests for:
- The correct handling of substitutions outside the base set.
- The invariant nature of the base set upon substitution.
- Proper handling when the condition is related or unrelated to the substitution.
- Correct behavior of the 'in' operator in `ConditionSet`.
- Evaluation and simplification of conditions leading to a logically empty set.

Each assertion attempt is enclosed in a `try-except` block to catch `AssertionError`s, and upon catching, utilizes the `print_stacktrace` function to display relevant debugging information. This setup ensures that issues are not only identified but also presented in a manner conducive to debugging and resolution.