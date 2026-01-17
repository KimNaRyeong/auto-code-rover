from sympy import geometry as ge, sympify
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

point1 = ge.Point(0, 0)
point2 = ge.Point(1, 1)

try:
    result = point1 + sympify(2.0) * point2
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue reproduced"

print(result)
