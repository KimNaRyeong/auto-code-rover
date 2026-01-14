from sympy import *
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    expected_result = S.false == S(0.0)
    actual_result = S(0.0) == S.false
    assert expected_result == actual_result
except AssertionError:
    print_stacktrace(AssertionError("S(0.0) == S.false returns True, while S.false == S(0.0) returns False"))
    sys.exit(1)

sys.exit(0)
