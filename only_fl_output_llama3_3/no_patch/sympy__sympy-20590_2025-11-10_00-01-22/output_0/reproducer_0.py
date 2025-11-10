import sympy
from unittest import TestCase

class Reproducer(TestCase):
    def test_symbol_dict(self):
        try:
            sym = sympy.Symbol('s')
            sym.__dict__
            self.fail("Expected AttributeError")
        except AttributeError as e:
            print_stacktrace(e)
            raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    Reproducer().test_symbol_dict()
