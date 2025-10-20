```python
import sys
from sympy import symbols, Eq, exp, solve, Function

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
    from sympy import idiff
    x, y = symbols('x y')
    f = Function('f')(x)  # Define a function f(x)

    # Test case: idiff with Eq
    try:
        result = idiff(Eq(y*exp(y), x*exp(x)), y, x)
    except Exception as e:
        print_stacktrace(e)
        assert False, "idiff does not support Eq correctly"

    # Test case: idiff with f(x) instead of y
    try:
        result = idiff(f*exp(f) - x*exp(x), f, x)
    except ValueError as e:
        print_stacktrace(e)
        assert False, "idiff does not support f(x) instead of y"
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected error while testing idiff with f(x)"

    # If both tests pass
    print("All tests passed successfully.")

if __name__ == "__main__":
    try:
        test_idiff_supports_eq_and_function_of_x()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    except Exception as general_exception:
        print(f"Unhandled exception: {general_exception}")
        sys.exit(1)
    else:
        sys.exit(0)
```