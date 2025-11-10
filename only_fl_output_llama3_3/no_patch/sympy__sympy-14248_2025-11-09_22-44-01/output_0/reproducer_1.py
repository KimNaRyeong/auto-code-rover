import sympy as sp
from functools import wraps

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

def assert_reproduces_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)  # Exit with code 0 when the issue is fixed
        except Exception as e:
            print_stacktrace(e)
            exit(1)
    return wrapper

@assert_reproduces_issue
def reproduce_issue():
    A = sp.MatrixSymbol('A', 2, 2)
    B = sp.MatrixSymbol('B', 2, 2)
    assert str(A - A*B - B) == f"A - {A*B} - B"
    pprint(A - A*B - B)
    latex(A - A*B - B)

if __name__ == "__main__":
    reproduce_issue()
