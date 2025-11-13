from sympy import symbols, I

def test_extract_multiplicatively():
    x, y = symbols('x y')
    expr1 = -2*x - 4*y - 8
    result = expr1.extract_multiplicatively(-2)
    assert result == -(x + 2*y + 4), "Expected extraction to succeed"

    expr2 = -2 - 4*I
    result = expr2.extract_multiplicatively(-2)
    assert result == -(1 + 2*I), "Expected extraction to succeed"

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
