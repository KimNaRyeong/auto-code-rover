import sympy as sp
from sympy import symbols, Idx

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

m, n = symbols("m, n", real=True)
try:
    i = sp.Idx("i", (n, m))
    raise AssertionError("Expected TypeError")
except Exception as e:
    print_stacktrace(e)
    exit(1)
