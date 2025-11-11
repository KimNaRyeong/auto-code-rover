import sympy
from unittest import TestCase

class Reproducer(TestCase):
    def test_symbol_dict(self):
        try:
            sym = sympy.Symbol('s')
            sym.__dict__
        except AttributeError as e:
            print_stacktrace(e)
            self.fail("Expected 'Symbol' object has no attribute '__dict__'")
        else:
            raise AssertionError("Expected 'AttributeError' but got nothing")

if __name__ == "__main__":
    Reproducer().test_symbol_dict()
