import sys
import traceback
import sympy as sp

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))

try:
    evaled_q = q.evalf()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

expected_output = sp.sympify("sqrt(2)/2 + 0*I + 0*J + sqrt(2)/2*K")

if evaled_q != expected_output:
    raise AssertionError(f"Unexpected output from evalf: {evaled_q} != {expected_output}")
