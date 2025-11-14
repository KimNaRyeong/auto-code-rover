import sys
from sympy.parsing.mathematica import parse_mathematica

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
    parse_mathematica('λ')
except Exception as e:
    print_stacktrace(e)
    assert False, "parse_mathematica cannot handle Greek characters"
sys.exit(1)

sys.exit(0)
