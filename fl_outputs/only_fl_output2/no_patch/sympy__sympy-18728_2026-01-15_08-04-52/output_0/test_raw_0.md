Certainly! Here's a Python script named `reproducer.py` which you can place in the root directory of your project. This script will test the specific behavior described in your issue with `Pow.is_zero` and `Pow.is_positive` and will use `print_stacktrace` to show a detailed traceback if any assertion fails due to the issue being present. When the issue is fixed, it should exit with code 0 without printing anything.

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

def test_pow_is_zero_is_positive():
    from sympy import symbols, oo

    a, b = symbols('a b', positive=True)
    try:
        # Testing is_zero and is_positive for Pow
        assert (a**b).is_zero is None, "Pow(a, b).is_zero should be None when a or b could be infinite"
        assert (a**b).is_positive is None, "Pow(a, b).is_positive should be None when a or b could be infinite or when a**b could be zero"

        # Specific checks for issue #9532
        n = symbols('n', real=True, finite=True)
        assert (1/n).is_zero is False, "1/n.is_zero should be False when n is real and finite"
        assert (oo/n).is_finite is False, "oo/n should not be considered finite when n is finite"

    except AssertionError as error:
        print_stacktrace(error)
        exit(1)

if __name__ == "__main__":
    test_pow_is_zero_is_positive()
    print("All tests passed successfully!")
```

This script checks both the general improvements proposed in the PR description and the specific edge case mentioned under `Other comments`. The assertion should trigger an error if the issue described is present, showing exactly where the problem occurred. When you run this script after applying the proposed changes (or in a context where the issue does not exist), it should complete successfully, verifying that the issue has been resolved.
