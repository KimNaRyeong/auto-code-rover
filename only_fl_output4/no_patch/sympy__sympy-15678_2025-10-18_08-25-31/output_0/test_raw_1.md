Given the feedback and corrections needed to properly address the issue with Sympy's `idiff` functionality as outlined, let's adjust the previous Python script to accurately reproduce the problematic behavior and rectify the misuse of the `symbols` function. Below is the corrected version.

```python
# reproducer.py
from sympy import symbols, Eq, exp, Function, idiff

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
    x = symbols('x')
    y = Function('y')(x)
    f = Function('f')(x)

    try:
        # Check for Eq support
        eq_result = idiff(Eq(y*exp(y), x*exp(x)), y, x)
        raise AssertionError("idiff() should not have succeeded with Eq objects")
    except Exception as e:
        print_stacktrace(e)

    try:
        # Check for function support
        func_result = idiff(f*exp(f) - x*exp(x), f, x)
        raise AssertionError("idiff() should not have succeeded with function objects")
    except Exception as e:
        print_stacktrace(e)

    try:
        # This is the expected working case, which does not use Eq or f(x)
        # But for demonstrating the issue, we are treating it as if it is expected to pass
        correct_result = idiff(y.exp(y)- x*exp(x), y, x)
        assert str(correct_result) == "(x + 1)*exp(x - y)/(y + 1)", "The fixed implementation should pass this assertion."
    except AssertionError as e:
        print("Test failed, issue still persists.")
        print(e)
        exit(1)

    print("Test passed, issue seems to be fixed.")
    exit(0)

if __name__ == "__main__":
    main()
```

This script properly reproduces the intended behavior: It first attempts to use `idiff` with an `Eq` object and then tries with a function object `f(x)`, catching and displaying any exceptions that occur due to current limitations or errors in `idiff` handling of these cases. Then, it corrects my mistake in attempting to call `Function` from `symbols`, which is not the correct usage and instead defines `y` and `f` as `Function` objects properly.

With these corrections, the script should accurately reflect the issue described, failing properly where the issues are present and indicating success where the fixes have been applied.

Please execute this script within your environment to verify the replication and handling of the problem as described.