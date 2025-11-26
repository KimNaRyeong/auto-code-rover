import sympy as sp
from sympy import symbols, sin

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

x = symbols('x')

try:
    ccode_result = sp.ccode(sp.sinc(x))
    assert ccode_result != '// Not supported in C:\n// sinc\nsinc(x)', "ccode(sinc(x)) should not return 'Not supported in C'"
    raise AssertionError("ccode(sinc(x)) did not return the expected result")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
