Here is the reproducer script:

```py
import math
from fractions import Fraction
from sympy import Rational, sqrt

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
    result = (sqrt(8))**Rational(2, 3)
    assert result == 2
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue not present")
    exit(0)
```

This script will run the expression `sqrt(8)**Rational(2, 3)` and check if the result is equal to `2`. If it's not, an `AssertionError` will be raised, which will trigger the `print_stacktrace` function to print the stack trace. The script will then exit with code 1.