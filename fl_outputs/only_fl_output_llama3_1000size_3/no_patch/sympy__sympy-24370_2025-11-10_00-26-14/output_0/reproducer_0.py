import sympy
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestSympyIssue(unittest.TestCase):

    def test_issue(self):
        f = StringIO()
        with redirect_stdout(f):
            try:
                s0 = sympy.Symbol('s0')
                sympy.Integer(1024)//s0
                self.fail("Expected TypeError")
            except TypeError as e:
                print_stacktrace(e)
                self.assertTrue(True)

    def test_issue_fixed(self):
        f = StringIO()
        with redirect_stdout(f):
            try:
                s0 = sympy.Symbol('s0')
                1024//s0
                self.fail("Expected TypeError")
            except TypeError as e:
                print_stacktrace(e)
                self.assertFalse(True)

if __name__ == '__main__':
    unittest.main()
