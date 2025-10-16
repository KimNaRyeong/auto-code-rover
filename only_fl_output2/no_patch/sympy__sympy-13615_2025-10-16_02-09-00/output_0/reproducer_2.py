from sympy import FiniteSet, Interval, Symbol, Complement
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

x = Symbol('x')
y = Symbol('y')

a = FiniteSet(x, y, 2)
b = Interval(-10, 10)

try:
    result = Complement(a, b)
    # Adjust the assertion to correctly match the expected output
    assert result == FiniteSet(x, y, 2), "Incorrect Complement result"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error status to indicate the issue is not solved
except Exception as e:
    print_stacktrace(e)
    sys.exit(2)  # Indicates a different error occurred

print("Success: The issue is fixed.")
sys.exit(0)
