import sympy as sp
from sympy import Quaternion

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
    q = Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
    result = q.evalf()
    assert str(result) == "sqrt(2)/2 + 0*I + 0*J + sqrt(2)/2*K", "evalf method did not return the expected string representation"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Quaternion class has no overridden evalf method")
