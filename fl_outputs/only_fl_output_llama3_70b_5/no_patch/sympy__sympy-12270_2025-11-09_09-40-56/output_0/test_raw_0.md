Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
from sympy import symbols, I
x, y = symbols('x y')

def test_extract_multiplicatively():
    expr1 = 2 + 4*I
    assert expr1.extract_multiplicatively(2) == 1 + 2*I

    expr2 = -2 - 4*I
    assert expr2.extract_multiplicatively(-1) == 2 + 4*I
    try:
        expr2.extract_multiplicatively(-2)
        raise AssertionError("Expected extraction to fail")
    except Exception as e:
        print_stacktrace(e)

    expr3 = 2*x + 4*y + 8
    assert expr3.extract_multiplicatively(2) == x + 2*y + 4

    expr4 = -2*x - 4*y - 8
    assert expr4.extract_multiplicatively(2) == -x - 2*y - 4
    assert expr4.extract_multiplicatively(-1) == 2*x + 4*y + 8
    try:
        expr4.extract_multiplicatively(-2)
        raise AssertionError("Expected extraction to fail")
    except Exception as e:
        print_stacktrace(e)

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
    test_extract_multiplicatively()
```
This script will raise an `AssertionError` when the issue is present, and print a stack trace of the issue. If the issue is fixed, the script will exit with code 0.