Here is the `reproducer.py` file that reproduces the issue:
```
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
```
This script imports Sympy, defines a test function `test_codegen_sign` that generates the Fortran code for the sign function using `sp.fcode(sp.sign(x))`. It then asserts that the generated code contains either "sign(1, x)" or "sign(1d0, x)", which is the valid Fortran syntax.

If the assertion fails, it catches the `AssertionError` exception and prints the stack trace using the provided `print_stacktrace` function. The script exits with code 1 in this case.

If the issue is not present (i.e., the generated code is valid), the script prints a success message and exits with code 0.