import sys
import traceback
from sympy import latex, symbols, Function, S

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols('x')
inv_trig_table = ["asin", "acos", "atan", "acot"]
Function("acsc")(x)

try:
    latex(Function("acsc")(x), inv_trig_style="full")
except Exception as e:
    print_stacktrace(e)
    sys.exit(0)

assert False, "The issue was not reproduced"
