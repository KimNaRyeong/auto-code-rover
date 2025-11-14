from sympy.parsing.mathematica import mathematica, parse_mathematica
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
    mathematica('λ')  # This should work
    parse_mathematica('λ')  # This should raise an exception
except Exception as e:
    print_stacktrace(e)
    assert False, "parse_mathematica cannot parse Greek characters"
else:
    sys.exit(0)
