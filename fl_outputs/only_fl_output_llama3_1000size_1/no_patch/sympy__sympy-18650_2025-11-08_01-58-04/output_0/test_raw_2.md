I apologize for the mistake earlier. Here is a new reproducer script that should reproduce the issue:

```py
from fractions import Fraction
import math

def reproduce_issue():
    result = (math.sqrt(8)) ** Fraction(2, 3)
    assert str(result) != '2', "sqrt(8)**Rational(2, 3) doesn't simplify"

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue reproduced successfully.")
    exit(0)

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
```

This script checks that the result of `sqrt(8)**Rational(2, 3)` is not equal to '2' as a string. If it is, then an AssertionError will be raised and the stack trace will be printed.