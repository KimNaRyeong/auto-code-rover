# reproducer.py
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

def check_issue():
    from sympy import S
    # Comparing 0.0 with false.
    condition1 = S(0.0) == S.false
    condition2 = S.false == S(0.0)
    
    # Expecting both conditions to have the same value.
    assert condition1 == condition2, "Comparisons between S(0.0) and S.false return inconsistent results."

try:
    check_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error code to indicate the presence of the issue
else:
    print("No issues detected. The comparison behaves as expected.")
    sys.exit(0)  # Normal exit with no errors
