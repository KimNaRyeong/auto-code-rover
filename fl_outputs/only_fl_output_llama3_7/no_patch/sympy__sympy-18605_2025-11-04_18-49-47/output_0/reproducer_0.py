import sympy as sp
import sys
from traceback import extract_tb, print_exception

def print_stacktrace(e: Exception):
    tb = extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    m, n = sp.symbols("m, n", real=True)
    i = sp.Idx("i", (m, n))
    assert False, "Expected TypeError"
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
