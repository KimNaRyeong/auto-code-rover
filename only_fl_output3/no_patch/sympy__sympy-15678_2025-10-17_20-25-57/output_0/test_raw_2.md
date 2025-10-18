Given your requirements, here is how you can write a `reproducer.py` file tailored to meet the needs of identifying whether the issue with `idiff` not supporting `Eq` and function of `x` remains or is resolved. The script raises an `AssertionError` when the issues are present and aims to exit with code 0 when the issues are resolved, printing a relevant stack trace upon encountering exceptions:

```python
# reproducer.py
from sympy import symbols, Function, Eq, exp, idiff
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_idiff_with_eq():
    x, y = symbols('x y')
    try:
        result = idiff(Eq(y*exp(y), x*exp(x)), y, x)
        print("idiff supports Eq successfully.")
    except Exception as e:
        print("idiff does not support Eq as expected:")
        print_stacktrace(e)
        raise AssertionError("idiff does not support Eq") from e

def test_idiff_with_function():
    x = symbols('x')
    f = symbols('f', cls=Function)(x)
    try:
        result = idiff(f*exp(f) - x*exp(x), f, x)
        print("idiff supports f(x) successfully.")
    except Exception as e:
        print("idiff does not support function of x (f(x)) as expected:")
        print_stacktrace(e)
        raise AssertionError("idiff does not support function of x") from e

def main():
    try:
        test_idiff_with_eq()
        test_idiff_with_function()
    except AssertionError as error:
        sys.exit(1)  # Exit with an error code, indicating the issue was reproduced.
    except Exception as general_error:
        print("An unexpected error occurred:", general_error)
        sys.exit(1)
    else:
        print("No issue detected with idiff. Exiting with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    import traceback
    main()
```

This script attempts to reproduce the reported issues by:

1. Testing `idiff` with an equation (`Eq`) to see if it can process such inputs without errors.
2. Testing `idiff` with a function of `x` (like `f(x)`) to check if it supports such expressions properly.

If `idiff` fails in either of these cases due to its inability to handle `Eq` or a function of `x`, the script prints the stack trace of the exception using the provided `print_stacktrace` function and exits with code `1`, indicating a failure due to issue reproduction. If no errors are encountered, it implies the issues might have been fixed, and it exits with code `0`.