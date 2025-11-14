import sympy as sp
from sympy import Symbol, Matrix, eye

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
    x = Symbol('x')
    M = Matrix([[x, 0, 1], [x, 0, 2], [sp.exp(x), 1, 0]])
    try:
        eigenvalues = M.eigenvals()
        assert eigenvalues != {}, "Eigenvalues should not be an empty dictionary"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected eigenvalues to be computed correctly")

if __name__ == "__main__":
    main()
