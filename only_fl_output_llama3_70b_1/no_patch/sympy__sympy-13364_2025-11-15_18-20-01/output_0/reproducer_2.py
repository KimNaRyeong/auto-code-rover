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

try:
    pow(sp.S(2), sp.S(3), sp.S(5))
except TypeError as e:
    if str(e) == "__sympifyit_wrapper() takes exactly 2 arguments (3 given)":
        print_stacktrace(e)
    else:
        raise AssertionError("Expected '__sympifyit_wrapper() takes exactly 2 arguments (3 given)' but got different error message")
