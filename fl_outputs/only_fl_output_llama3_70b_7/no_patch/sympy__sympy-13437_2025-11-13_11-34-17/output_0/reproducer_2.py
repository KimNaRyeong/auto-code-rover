import sympy as sp

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

n = sp.symbols('n')
result = sp.bell(n).limit(n, sp.oo)

try:
    assert result == sp.oo
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("The issue is fixed.")
    exit(0)
