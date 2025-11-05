import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_degree(self):
        try:
            result = sp.degree((sp.Symbol('x')-2)/(sp.sympify('x**2+1')), sp.Symbol('x'))
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == "__main__":
    test_case = Reproducer()
    test_case.test_degree()
