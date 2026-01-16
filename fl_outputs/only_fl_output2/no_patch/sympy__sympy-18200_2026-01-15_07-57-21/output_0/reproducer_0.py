# reproducer.py
from sympy import ImageSet, Lambda, S
from sympy.abc import n

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

def check_issue():
    try:
        result = ImageSet(Lambda(n, n**2), S.Integers).intersect(S.Integers)
        print("The issue appears to be fixed.")  # This line should not execute if the issue is present
        return True
    except Exception as e:
        print_stacktrace(e)
        return False

# Assert that the issue exists
assert not check_issue(), "The issue has been fixed."

