import sympy
import unittest
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestIssue(unittest.TestCase):

    def test_issue(self):
        x, y = sympy.symbols('x, y')
        expected_result1 = (0, 0)
        expected_result2 = (-4.07992766242527e+17*y, 1.0*y)
        expected_result3 = (0, 0)

        result1 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 * x)], (x, y))
        if result1 != expected_result1:
            raise AssertionError("linsolve failed for the first system of equations")
            print_stacktrace(e)

        result2 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0216 * x)], (x, y))
        if result2 != expected_result2:
            raise AssertionError("linsolve failed for the second system of equations")
            print_stacktrace(e)

        result3 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0217 * x)], (x, y))
        if result3 != expected_result3:
            raise AssertionError("linsolve failed for the third system of equations")
            print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
