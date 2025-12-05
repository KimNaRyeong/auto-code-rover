import sys
import traceback
from sympy import *

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

n = symbols('n')
result = bell(n).limit(n, oo)
expected_result = oo

if result != expected_result:
    raise AssertionError(f"Expected bell(oo) to be oo, but got {result} instead.")
    print_stacktrace(Exception("Expected bell(oo) to be oo, but got " + str(result) + " instead."))
