Here is the reproducer script:

```python
import sympy
import unittest
from io import StringIO
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

class TestLinsolve(unittest.TestCase):

    def test_linsolve(self):
        x, y = sympy.symbols('x, y')
        expected_result1 = (0, 0)
        expected_result2 = (-4.07992766242527e+17*y, 1.0*y)
        expected_result3 = (0, 0)

        result1 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 * x)], (x, y))
        if result1 != expected_result1:
            raise AssertionError("linsolve failed for 0.0215*x")
            print_stacktrace(e)

        result2 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0216 * x)], (x, y))
        if result2 != expected_result2:
            raise AssertionError("linsolve failed for 0.0216*x")
            print_stacktrace(e)

        result3 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0217 * x)], (x, y))
        if result3 != expected_result3:
            raise AssertionError("linsolve failed for 0.0217*x")
            print_stacktrace(e)

if __name__ == '__main__':
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        unittest.main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```

This script will run the test cases and if any of them fail, it will raise an `AssertionError`, print the stack trace, and exit with code 1. If all tests pass, it will exit with code 0.