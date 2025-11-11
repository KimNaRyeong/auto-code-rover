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

try:
    import sympy
    q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
    f = StringIO()
    with redirect_stdout(f):
        q.evalf()
    output = f.getvalue().strip()
    if not output.startswith('sqrt(2)/2 + 0*i + 0*j + sqrt(2)/2*k'):
        raise AssertionError("Quaternion class has no overridden evalf method")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully. Quaternion class does not have an overridden evalf method.")
exit(0)
