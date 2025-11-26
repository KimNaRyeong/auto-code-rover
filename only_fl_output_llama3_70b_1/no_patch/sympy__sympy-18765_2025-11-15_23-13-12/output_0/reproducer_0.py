import sympy as sp
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
    x = sp.Symbol('x')
    A = sp.MatrixSymbol('A', 2, 2)

    # Test Add with evaluate=True
    result = Add(x, x, evaluate=True)
    assert result == 2*x, f"Expected Add(x, x, evaluate=True) to return 2*x, but got {result}"
    
    # Test MatAdd without evaluate keyword
    result = MatAdd(A, A)
    assert result != 2*A, f"Expected MatAdd(A, A) to not return 2*A, but got {result}"
    
    # Test MatAdd with evaluate=True
    try:
        result = MatAdd(A, A, evaluate=True)
        assert result == 2*A, f"Expected MatAdd(A, A, evaluate=True) to return 2*A, but got {result}"
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("MatAdd does not support evaluate keyword") from e

if __name__ == "__main__":
    main()
