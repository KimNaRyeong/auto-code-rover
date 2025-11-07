import sympy as sp
from io import StringIO
from contextlib import redirect_stdout

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

def reproduce_issue():
    x1 = sp.symbols('x_{1}')
    f = StringIO()
    with redirect_stdout(f):
        try:
            print(x1)
        except Exception as e:
            print_stacktrace(e)
            raise
    output = f.getvalue().strip()
    if "x_{1," not in output:
        raise AssertionError("Expected 'x_{1,' but got: " + output)

if __name__ == "__main__":
    reproduce_issue()
