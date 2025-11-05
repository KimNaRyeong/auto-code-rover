Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import z, pi
import unittest

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

class TestPolylogExpansion(unittest.TestCase):

    def test_polylog_expansion(self):
        try:
            self.assertEqual(sp.nsimplify(expand_func(polylog(2, Rational(1, 2))).evalf(), [pi**2, log(2)**2]), '-log(2)**2/2 + pi**2/12')
        except AssertionError as e:
            print_stacktrace(e)
            raise

    def test_polylog_expand_func(self):
        try:
            expand_func(polylog(1, z))
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected an AssertionError")

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` module to define two tests. The first test checks if the expansion of `polylog(2, Rational(1, 2))` is correct. If it's not, it prints a stack trace and raises an `AssertionError`. The second test tries to expand `polylog(1, z)` and catches any exceptions that occur. If an exception occurs, it prints a stack trace and fails the test.

To run this script, save it in a file named `reproducer.py`, then execute it with `python3 reproducer.py`.