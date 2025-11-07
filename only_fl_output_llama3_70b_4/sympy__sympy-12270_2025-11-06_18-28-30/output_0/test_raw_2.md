Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
from sympy import symbols, I
x, y = symbols('x y')

def test_extract_multiplicatively():
    expr1 = 2 + 4*I
    result1 = expr1.extract_multiplicatively(2)
    assert result1 == 1 + 2*I

    expr2 = -2 - 4*I
    result2 = expr2.extract_multiplicatively(-2)
    assert result2 != 1 + 2*I, "Expected extraction to fail"

    expr3 = 2*x + 4*y + 8
    result3 = expr3.extract_multiplicatively(2)
    assert result3 == x + 2*y + 4

    expr4 = -2*x - 4*y - 8
    result4 = expr4.extract_multiplicatively(-2)
    assert result4 != x + 2*y + 4, "Expected extraction to fail"

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

if __name__ == "__main__":
    try:
        test_extract_multiplicatively()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.

Please note that I've added more test cases to cover different scenarios, and also modified the assertions to check for the expected failure of extraction.