import sympy as sm
from collections import defaultdict

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
    M = sm.eye(6)
    V = 2 * sm.ones(6, 2)
    result = M.col_insert(3, V)
    assert result.shape == (6, 4), "Matrix shape is incorrect"
except Exception as e:
    print_stacktrace(e)
    raise
