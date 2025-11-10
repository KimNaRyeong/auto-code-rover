Here is the reproducer script:

```py
import math
from fractions import Fraction
from assertpy import assert_that

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

def reproduce_issue():
    result = math.sqrt(8) ** Fraction(2, 3)
    assert_that(result).is_equal_to(2)

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue reproduced successfully.")
    exit(0)
```

This script will run the reproducer function and check if the assertion fails. If it does, it will print the stack trace and exit with code 1. If not, it will print a success message and exit with code 0.