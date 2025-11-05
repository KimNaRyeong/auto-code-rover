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
    import sympy
    from sympy.abc import x
    assert sp.fcode(sp.sign(x)) == 'sign(1, x)', f"Expected 'sign(1, x)' but got {sp.fcode(sp.sign(x))}"
except Exception as e:
    print_stacktrace(e)
    raise
else:
    print("Test passed")
    exit(0)
