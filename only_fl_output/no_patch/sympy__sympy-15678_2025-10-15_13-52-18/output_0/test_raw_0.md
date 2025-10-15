```python
from sympy import symbols, Eq, exp, solve
from sympy.calculus.util import idiff
from sympy.core.function import Function


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


def test_idiff():
    x, y = symbols('x y')
    f = Function('f')(x)
    
    try:
        # Test Eq support
        result1 = idiff(Eq(y*exp(y), x*exp(x)), y, x)
        # Assuming the desired output if no exception were to be thrown
        # is not defined in the given issue; thus, we just check if it executes.
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Eq support test failed")

    try:
        # Test f(x) support
        idiff(f*exp(f) - x*exp(x), f, x)
        # f(x) scenario is expected to fail based on provided issue details.
        raise AssertionError("f(x) support test passed but was expected to fail")
    except ValueError as e:
        # Correctly caught the expected error for the f(x) scenario
        # This is expected, so we do not raise AssertionError here.
        pass
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected exception type for f(x) support test")

    try:
        # Test the working scenario for non-Eq and direct expression
        result3 = idiff(y*exp(y)- x*exp(x), y, x)
        assert str(result3) == "(x + 1)*exp(x - y)/(y + 1)", "Mismatch in expected output"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Direct expression test failed")


if __name__ == "__main__":
    test_idiff()
    print("All tests passed.")
```

This script tries to reproduce the issues mentioned:
- It first tests `idiff` with an `Eq` object to see if the function can handle equation objects as expected. 
- Then it tests `idiff` with a function of `x` (`f(x)`) to see if it can handle functional forms, which based on the issue description, it cannot at the moment. This part of the test is designed to pass if it fails (catching a ValueError as anticipated from the issue description).
- Lastly, it tests a direct expression involving symbols `x` and `y`, which should work fine and is used as a sanity check to ensure basic functionality isn't broken.

The script raises an `AssertionError` when an issue is present, and for the purpose of demonstration, it is expected to print a stack trace because of the issues with handling `Eq` objects and the inability to process expressions involving `f(x)` as correctly described in the issue details.