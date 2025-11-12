import sympy as sp
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

m, n = sp.symbols("m, n", real=True)

try:
    i = sp.Idx("i", (m, n))
    assert False, "Idx object should not accept non-integer bounds"
except TypeError as e:
    print_stacktrace(e)
else:
    sys.exit(1)

sys.exit(0)
