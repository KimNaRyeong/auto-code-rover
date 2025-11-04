import sympy
from io import StringIO
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    for i in range(3):
        x, y = sympy.symbols('x, y')
        result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 + 0.0001 * i * x)], (x, y))
        if str(result) != "FiniteSet((0, 0))":
            raise AssertionError("linsolve failed for 0.0215 + 0.0001 * i * x")
        print_stacktrace(e)

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    sys.exit(0)
