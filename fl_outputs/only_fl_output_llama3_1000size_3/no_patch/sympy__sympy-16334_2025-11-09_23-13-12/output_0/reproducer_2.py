import sympy as sp
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    from sympy import symbols, ask, Q
    x = sp.symbols('x')
    p = sp.symbols('p', real=True, zero=False)
    q = sp.symbols('q', zero=True)
    assert not (0**q).is_positive
except AssertionError as e:
    print_stacktrace(e)
    raise

sys.exit(0 if not sys.exc_info() else 1)
