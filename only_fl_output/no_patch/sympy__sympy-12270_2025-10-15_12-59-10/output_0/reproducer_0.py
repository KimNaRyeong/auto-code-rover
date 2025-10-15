from sympy import symbols, I, Mul
from typing import NoReturn

def print_stacktrace(e: Exception) -> NoReturn:
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

def test_extract_multiplicatively():
    x, y = symbols('x y')
    
    assert (2 + 4*I).extract_multiplicatively(2) == 1 + 2*I
    
    assert (-2 - 4*I).extract_multiplicatively(-1) == 2 + 4*I
    
    # Issue here
    try:
        result = (-2 - 4*I).extract_multiplicatively(-2)
        assert result is not None, "Failed to extract multiplicatively."
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # Similar issue with symbolic expressions
    try:
        result = (-2*x - 4*y - 8).extract_multiplicatively(-2)
        assert result is not None, "Failed to extract multiplicatively from symbolic expression."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_extract_multiplicatively()
    except AssertionError:
        exit(1)
    print("All tests passed successfully.")
    exit(0)
