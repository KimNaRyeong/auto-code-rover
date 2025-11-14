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

def reproduce_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")
    return wrapper

@reproduce_issue
def main():
    import sympy as sp
    I = sp.I
    M = sp.MatrixSymbol('M', 2, 2)
    print(I * M)

if __name__ == "__main__":
    main()
