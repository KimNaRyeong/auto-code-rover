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
    f = StringIO()
    with redirect_stdout(f):
        try:
            sp.OneMatrix(1, 2).str()
            sp.ZeroMatrix(1, 2).pretty()
            sp.Identity(3).mathml()
        except AttributeError as e:
            raise AssertionError("Issue not reproduced") from e

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
