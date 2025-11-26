import sympy
from sympy import Add, MatAdd, Symbol, MatrixSymbol

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

def main():
    x = sympy.Symbol('x')
    A = sympy.MatrixSymbol('A', 2, 2)

    # Test Add with evaluate=True
    result = Add(x, x, evaluate=True)
    assert result == 2*x, "Add with evaluate=True failed"

    # Test MatAdd without evaluate keyword
    result = MatAdd(A, A)
    assert result != 2*A, "MatAdd without evaluate keyword failed (should not be canonicalized)"

    # Test MatAdd with evaluate=True
    try:
        result = MatAdd(A, A, evaluate=True)
        assert result == 2*A, "MatAdd with evaluate=True failed"
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("MatAdd with evaluate=True should not raise a TypeError")

if __name__ == "__main__":
    main()
