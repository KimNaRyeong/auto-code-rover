import sympy
from sympy.abc import x
import unittest

class TestNonCommutativePowSubs(unittest.TestCase):

    def test_noncommutative_pow_subs(self):
        sympy.__version__ = '1.1'
        x = sympy.Symbol('x', commutative=False)
        self.assertRaises(AssertionError, lambda: (x*x*x).subs({x*x: 1}))

    def test_print_stacktrace(self):
        e = AssertionError("Test failed")
        print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
