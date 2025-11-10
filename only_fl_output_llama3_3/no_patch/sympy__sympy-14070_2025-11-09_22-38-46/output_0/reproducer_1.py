import sympy as sp
from sympy import log, simplify

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
    result = sp.log(sp.sympify('3')) - sp.log(sp.sympify('2'))
    assert simplify(result) == sp.log(3/2), "Expected log(3/2)"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed")
    exit(0)
