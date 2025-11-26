Here is the `reproducer.py` file that reproduces the issue:
```
import sympy

def test_float_constructor():
    try:
        # Try to create a Float with 54 binary digits
        f = sympy.Float(1.0, prec=54)
        assert False, "Expected ValueError or TypeError"
    except (ValueError, TypeError):
        pass  # Expected error

    # Check that the `prec` argument is currently decimal precision
    f = sympy.Float(1.0, 15)
    assert f._prec != 15, "Expected _prec to be different from decimal precision"

    print("Issue reproduced successfully")

if __name__ == "__main__":
    try:
        test_float_constructor()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 if the issue is present
    exit(0)  # Exit with code 0 if the issue is fixed

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
```
This script tries to create a `Float` object with 54 binary digits, which should raise an error. It then checks that the `prec` argument is currently decimal precision by creating a `Float` object with 15 decimal digits and checking that the `_prec` attribute is not equal to 15.

If the issue is present, the script will exit with code 1 and print a stack trace of the `AssertionError`. If the issue is fixed, the script will exit with code 0.