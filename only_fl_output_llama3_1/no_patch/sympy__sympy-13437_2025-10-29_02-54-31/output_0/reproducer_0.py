import sympy as sp
from sympy import symbols, oo
import unittest
from unittest.mock import patch
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestBellLimit(unittest.TestCase):

    @patch('sys.stdout.write')
    def test_bell_limit(self, mock_stdout):
        n = symbols('n')
        try:
            result = bell(n).limit(n, oo)
            self.assertEqual(result, oo)
        except Exception as e:
            print_stacktrace(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()
