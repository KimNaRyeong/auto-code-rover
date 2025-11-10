import sympy as sp
from sympy.abc import x

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
    code = sp.fcode(sp.sign(x))
    assert "sign(1, x)" in code or "sign(1d0, x)" in code, f"Invalid Fortran syntax for sign function: {code}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
