import sympy as sp
from sympy.abc import x

def test_codegen_sign():
    code = sp.fcode(sp.sign(x))
    assert "sign(1, x)" in code or "sign(1d0, x)" in code, f"Invalid Fortran syntax: {code}"

try:
    test_codegen_sign()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present. Exiting with code 0.")
exit(0)

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
