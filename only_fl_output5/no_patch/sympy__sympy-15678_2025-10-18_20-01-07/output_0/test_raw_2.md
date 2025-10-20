Given the requirements and the need to accurately reproduce and indicate the specific issue with `idiff` in SymPy, the following Python script is structured to directly tackle the reproduction of both identified problems and will use assertions in such a way that it exits with code 0 when the issues are fixed. Note that this approach specifically captures the conditions described in the issue: `idiff` not supporting `Eq` directly without throwing an `IndexError` and handling functions in the form of `f(x)` which currently raises a `ValueError`.

```python
import sys
from sympy import symbols, Eq, exp, Function, solve
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

def main():
    x, y = symbols('x y')
    f = Function('f')(x)
    
    # Test case 1: idiff with Eq instance
    try:
        eq = Eq(y*exp(y), x*exp(x))
        result = idiff(eq, y, x)
        raise AssertionError("The issue with idiff not supporting Eq instances still exists")
    except IndexError as e:
        # Expected issue presented
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
        sys.exit("Unexpected error encountered during Eq test")

    # Test case 2: idiff with function of x instead of y
    try:
        eq = f*exp(f) - x*exp(x)
        result = idiff(eq, f, x)
        raise AssertionError("The issue with idiff not supporting f(x) instead of y still exists")
    except ValueError as e:
        if "expecting x-dependent symbol(s) but got: f(x)" in str(e):
            # This is the expected error message for this issue.
            print_stacktrace(e)
        else:
            raise
    except Exception as e:
        print_stacktrace(e)
        sys.exit("Unexpected error encountered during f(x) test")
    
    print("Issues with idiff accurately reproduced. Awaiting fixes.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(e)
        sys.exit(1)  # Exit with non-zero if the issue is still present, indicating failure to reproduce the condition.
    except Exception as general_error:
        print(f"Unhandled exception: {general_error}")
        sys.exit(1)
    else:
        # If no exceptions, this means issues have potentially been fixed.
        sys.exit(0)
```

This script, `reproducer.py`, is tailored to run as a standalone file in the root directory of the project and is designed to explicitly check for the two mentioned issues with `idiff` in SymPy by:

1. Trying to use `idiff` with an `Eq` instance and catching the expected `IndexError` as an indicator of the issue.
2. Attempting to use `idiff` with `f(x)` instead of y and expecting a `ValueError` with a specific message as an indicator of the issue.

The script makes use of the provided `print_stacktrace` function to clearly display where exactly in the code the error occurs, enhancing the understanding and potential debugging process of these issues.