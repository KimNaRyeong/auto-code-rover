import sympy
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
    import sympy
    s0 = sympy.Symbol('s0')
    1024 // s0
    assert False, "Expected TypeError"
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue fixed")
    sys.exit(0)
