import sympy as sp
from sympy import symbols, oo
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestBellLimit(unittest.TestCase):

    def test_bell_limit(self):
        try:
            with redirect_stdout(StringIO()):
                n = symbols('n')
                bell_n = sp.bell(n)
                result = bell_n.limit(n, oo)
                self.assertEqual(result, oo)
        except Exception as e:
            print_stacktrace(e)
            raise
        else:
            exit(0)

if __name__ == '__main__':
    unittest.main()
