import sympy as sp
from sympy.utilities.codegen import ccode

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

x, theta = sp.symbols('x theta')

try:
    c_code = ccode(sp.sinc(x))
    assert 'sinc' not in c_code
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed")
exit(0)
