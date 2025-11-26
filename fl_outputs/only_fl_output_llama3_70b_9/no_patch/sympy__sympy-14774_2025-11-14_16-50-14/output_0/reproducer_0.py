import sympy as sp
from sympy import symbols, acsc, asec

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
    assert sp.latex(acsc(x), inv_trig_style="full") == '\\operatorname{arccsc}{\\left (x \\right )}'
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("Issue is fixed, exiting with code 0")
raise SystemExit(0)
