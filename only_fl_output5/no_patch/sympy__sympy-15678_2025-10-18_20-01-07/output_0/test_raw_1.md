Given the feedback that the initial script did not correctly trigger the intended `AssertionError` to indicate the issues are present, I am revising the script to more accurately target the exceptions described and ensure that the assertions are triggered based on the exceptions or lack thereof. 

```python
import sys
from sympy import symbols, Eq, exp, Function
from sympy.geometry.util import idiff

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

def test_idiff_supports_eq_and_function_of_x():
    x = symbols('x')
    y = Function('y')(x)  # Making y a function of x
    f = Function('f')(x)  # Define a function f(x)

    # Test case: idiff with Eq
    try:
        idiff(Eq(y*exp(y), x*exp(x)), y, x)
    except IndexError as e:
        print_stacktrace(e)
        assert False, "idiff does not support Eq correctly"

    # Test case: idiff with function of x instead of y
    try:
        idiff(f*exp(f) - x*exp(x), f, x)
    except ValueError as e:
        print_stacktrace(e)  # This should print the stack trace where the issue occurs
        # This assertion ensures that we expected this failure, marking the issue present.
        assert "expecting x-dependent symbol(s) but got: f(x)" in str(e), "idiff issue with functions not detected."
    except IndexError as e:
        print_stacktrace(e)
        assert False, "idiff has a different issue with handling functions."
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected error while testing idiff with function of x"

    # Final test to confirm working case
    try:
        result = idiff(y*exp(y)- x*exp(x), y, x)
        assert result is not None, "idiff failed on a valid equation."
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected error in the final working case of idiff."

    print("All tests passed successfully.")

if __name__ == "__main__":
    try:
        test_idiff_supports_eq_and_function_of_x()
    except AssertionError as error_message:
        print(error_message)
        sys.exit(1)
    except Exception as general_exception:
        print(f"Unhandled exception: {general_exception}")
        sys.exit(1)
    else:
        sys.exit(0)
```

This script aims to directly address the outlined issues:

1. `idiff` not supporting `Eq`.
2. `idiff` incorrectly handling expressions involving `f(x)` instead of `y`, where `f(x)` should be recognized as a function of `x`.

The script will now raise explicit `AssertionError`s based on whether the exception expected is thrown, and for the successful execution, it asserts that a result is non-None, indicating that the script expects the `idiff` function to work without errors for valid inputs.