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
    try:
        f = StringIO()
        with redirect_stdout(f):
            str(sp.Interval(0, 1))
            str(sp.FiniteSet(1, 2, 3))
        result = f.getvalue().strip()
        if not (result == "[0, 1]" and result == "{1, 2, 3}"):
            raise AssertionError("Expected output not matched")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
