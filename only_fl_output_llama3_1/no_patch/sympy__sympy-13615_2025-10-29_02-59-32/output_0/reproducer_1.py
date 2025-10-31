import sys
from sympy import FiniteSet, Interval, Complement  # Replace 'your_module' with the actual module name

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
    a = FiniteSet('x', 'y', 2)
    b = Interval(-10, 10)
    result = Complement(a, b)
    if str(result) != "{'x', 'y'} - set(range(-10, 11))":
        raise AssertionError("Expected {x, y} \ [-10,10] as output.")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not reproduced. All tests pass.")
sys.exit(0)
