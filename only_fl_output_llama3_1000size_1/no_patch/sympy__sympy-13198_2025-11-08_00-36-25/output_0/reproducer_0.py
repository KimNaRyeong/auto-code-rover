import sympy as sp
from sympy.abc import x, y, z
import unittest

def test_issue():
    try:
        z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
        w = sp.expand(z)
        v = sp.factor(w)
        assert round(v.evalf(subs={x: 1, y: 2}), 8) == 1e-8
    except AssertionError:
        print_stacktrace(sys.exc_info()[1])
        raise

class TestIssue(unittest.TestCase):
    def test_issue(self):
        try:
            test_issue()
            self.fail("Expected an assertion error")
        except SystemExit as e:
            if e.code != 0:
                print_stacktrace(e)
                raise

if __name__ == "__main__":
    unittest.main()
