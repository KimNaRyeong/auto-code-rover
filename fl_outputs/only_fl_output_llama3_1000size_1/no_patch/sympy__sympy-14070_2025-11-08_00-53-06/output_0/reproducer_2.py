import sympy as sp
from sympy.logic.boolalg import to_cnf

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
    result = sp.logcombine(sp.log(3) - sp.log(2))
    if not isinstance(result, type(sp.S)):
        raise AssertionError("logcombine(log(3) - log(2)) should return log(3/2) but it doesn't.")
except Exception as e:
    print_stacktrace(e)
    raise
else:
    exit(0)
