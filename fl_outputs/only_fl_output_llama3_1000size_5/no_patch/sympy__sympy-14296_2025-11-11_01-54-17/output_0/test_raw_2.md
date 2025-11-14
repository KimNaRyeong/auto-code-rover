Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

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

class Reproducer(TestCase):
    def test_issue(self):
        b = 1 - sp.sqrt(2)
        a = sp.to_number_field(b)
        if not (a.minpoly == sp.Poly([1, -2, -1], 'x')):
            raise AssertionError("Issue present")
        print_stacktrace(AssertionError("Issue fixed"))

if __name__ == "__main__":
    try:
        Reproducer().test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed, exiting with code 0.")
        exit(0)

```

This script creates the algebraic number `b = 1 - sqrt(2)` and then calls `to_number_field` to create an `AlgebraicNumber` generating the extension field. It checks if the minimal polynomial of this `AlgebraicNumber` is correct, and if not, it raises an `AssertionError`. The script also prints a stack trace for the error message.

Please note that you may need to install sympy library before running this script.