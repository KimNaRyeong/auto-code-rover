import sympy as sp
from sympy import Symbol, Matrix, eye
from functools import wraps

def assert_raises(expected_exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except expected_exception as e:
                print_stacktrace(e)
                raise AssertionError("Expected exception not raised")
            else:
                raise AssertionError("Expected exception not raised")
        return wrapper
    return decorator

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

@assert_raises(sp.matrices.MatrixError)
def reproduce_issue():
    x = Symbol('x')
    M = Matrix([[x, 0, 1], [x, 0, 2], [sp.exp(x), 1, 0]])
    try:
        M.eigenvals()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
