Here is the reproducer script:

```py
import math
from fractions import Fraction

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
    try:
        result = (math.sqrt(8)) ** Fraction(2, 3)
        assert result == 2
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the expression `(math.sqrt(8))**Fraction(2, 3)` and check if the result is equal to `2`. If it's not, an `AssertionError` will be raised with a stack trace.