print("Reproducing issue...")

from sympy import *

n = symbols('n')
result = bell(n).limit(n, oo)

if result != oo:
    try:
        assert result == oo
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 if the issue is present

print("Issue not present. Test passed.")
sys.exit(0)  # Exit with code 0 if the issue is fixed.

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
