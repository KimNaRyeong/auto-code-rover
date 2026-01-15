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

def test_rational_calculation():
    from sympy import Rational

    # Test case with strings
    try:
        value_str = Rational('0.5', '100')
        # Expected behavior in sympy 1.8
        assert value_str == Rational(1, 200), f"Incorrect calculation for Rational('0.5', '100'): {value_str}"
    except AssertionError as e:
        print_stacktrace(e)

    # Test case with numbers
    try:
        value_num = Rational(0.5, 100)
        # Expected behavior
        assert value_num == Rational(1, 200), f"Incorrect calculation for Rational(0.5, 100): {value_num}"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_rational_calculation()
```
This script defines a function to print a stack trace for exceptions, specifically designed for understanding the flow of exceptions with line numbers and file names. Then, it moves on to define a test function that evaluates the behavior of `sympy.Rational`, addressing the issue that arises when initializing `Rational` with different types of arguments (string vs. numerical). The script tests two cases to ensure both `Rational('0.5', '100')` and `Rational(0.5, 100)` behave as expected, that is, evaluating to `Rational(1, 200)`.

When the issue described exists, the script should raise an `AssertionError` either for the string case, showing an incorrect calculation, or for the numerical case if it behaves unexpectedly. The `if __name__ == "__main__":` block ensures that the test cases are run only when the script is executed directly, and not when it's imported as a module in another script.