import sympy as sp
from sympy.abc import z, pi
import unittest

def test_polylog_expansion():
    assert str(sp.polylog(2, sp.Rational(1, 2)).expand(func=True).evalf()) == "-log(2)**2/2 + pi**2/12"

class TestPolylogExpansion(unittest.TestCase):
    def test_polylog_expansion(self):
        try:
            test_polylog_expansion()
            raise AssertionError("Expected an exception")
        except Exception as e:
            print_stacktrace(e)

if __name__ == "__main__":
    unittest.main()
