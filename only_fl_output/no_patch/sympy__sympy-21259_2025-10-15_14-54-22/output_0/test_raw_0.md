Certainly! The goal is to create a standalone Python script named `reproducer.py` that checks for the correctness of the `.as_relational` method of the `Range` class in SymPy. When the current issue exists, it should raise an `AssertionError` and print a stack trace detailing where the issue occurred in the script.

Here is the content for `reproducer.py` that meets your criteria:

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

def test_range_as_relational():
    from sympy import Range, Symbol, Eq, floor, Mod
    x = Symbol('x')
    correct_representation = (x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1)
    try:
        assert Range(3, 11, 2).as_relational(x) == correct_representation, "Incorrect relational representation for Range"
        print("Issue is fixed or not present.")
    except AssertionError as e:
        print_stacktrace(e)
        raise AssertionError("The issue with Range.as_relational is present.") from None

if __name__ == "__main__":
    try:
        test_range_as_relational()
    except AssertionError:
        exit(1)  # Exit with code 1 when issue is present
    else:
        exit(0)  # Exit with code 0 when issue is fixed or not present
```

In this script:
- `print_stacktrace()` is defined to print detailed error information.
- `test_range_as_relational()` checks if the `.as_relational` method for `Range` objects functions as expected according to the correct representation described in the issue.
- The main block runs the test, and based on the result, exits with code 1 if the issue is present (assertion failed) or exits with code 0 if the issue is not present or has been fixed.

**Note:** This script is designed to be run in the root directory of a project where SymPy is installed and accessible. Make sure SymPy is installed in your Python environment where you're planning to run this script.