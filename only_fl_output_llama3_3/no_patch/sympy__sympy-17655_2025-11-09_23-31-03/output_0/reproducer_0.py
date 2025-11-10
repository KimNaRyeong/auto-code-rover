import sympy
from sympy import geometry as ge
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

class TestReproducer(unittest.TestCase):

    def test_reproduce_issue(self):
        try:
            point1 = ge.Point(0, 0)
            point2 = ge.Point(1, 1)
            point1 + sympy.sympify(2.0) * point2
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected no exception")

    def test_expected_behaviour(self):
        try:
            point1 = ge.Point(0, 0)
            point2 = ge.Point(1, 1)
            point1 + point2 * sympy.sympify(2.0)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected no exception")

if __name__ == '__main__':
    unittest.main()
