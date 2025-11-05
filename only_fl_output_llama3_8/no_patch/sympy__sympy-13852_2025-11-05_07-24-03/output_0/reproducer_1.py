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
