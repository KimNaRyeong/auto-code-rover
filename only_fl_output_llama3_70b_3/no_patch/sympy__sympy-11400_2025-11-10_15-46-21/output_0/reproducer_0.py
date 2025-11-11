from sympy import symbols, sinc, ccode
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

x = symbols('x')

try:
    result = ccode(sinc(x))
    assert "sin(" in result, "ccode(sinc(x)) does not work as expected"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
