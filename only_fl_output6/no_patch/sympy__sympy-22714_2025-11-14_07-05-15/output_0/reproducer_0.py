# reproducer.py
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
    with sp.evaluate(False):
        # The code below is expected to run without error.
        # If it raises an exception, we catch it and print the stack trace.
        sp.S('Point2D(Integer(1),Integer(2))')
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("The issue is present")

# If no exception is raised, it means the issue is fixed or not present.
print("No error raised, issue might be fixed or not present.")
