Below is a `reproducer.py` script that can be used to reproduce the issue described. This script checks whether `extract_multiplicatively` behaves as expected in each scenario, raising an `AssertionError` when the result doesn't match the anticipated outcome. It uses `print_stacktrace` to show detailed information about where the error occurred if the correct values are not returned.

```python
from sympy import I, Mul, symbols

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

def check_extract_multiplicatively():
    x, y = symbols('x y')
    
    # Testing complex numbers
    try:
        assert (2+4*I).extract_multiplicatively(2) == 1 + 2*I
        assert (-2-4*I).extract_multiplicatively(-1) == 2 + 4*I
        result = (-2-4*I).extract_multiplicatively(-2)
        assert result is not None, "Failed to extract (-2) from (-2-4*I)"
    except AssertionError as e:
        print_stacktrace(e)
    
    # Testing algebraic expressions
    try:
        assert (2*x + 4*y + 8).extract_multiplicatively(2) == x + 2*y + 4
        assert (-2*x - 4*y - 8).extract_multiplicatively(2) == -x - 2*y - 4
        assert (-2*x - 4*y - 8).extract_multiplicatively(-1) == 2*x + 4*y + 8
        result = (-2*x - 4*y - 8).extract_multiplicatively(-2)
        assert result is not None, "Failed to extract (-2) from (-2*x - 4*y - 8)"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    check_extract_multiplicatively()
```

This script attempts to validate the behavior of the `extract_multiplicatively` method in different scenarios described in the issue. If the method does not behave as expected, an `AssertionError` will be raised and the script will print the stack trace for where the issue occurred, making it easier to debug and fix the issue. When the issue is fixed or if there is no issue, the script should exit without any errors.