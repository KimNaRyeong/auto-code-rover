import sympy
import unittest
from unittest.mock import patch

class C:
    def __repr__(self):
        return 'x.y'

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

class TestSympyEquality(unittest.TestCase):
    @patch('builtins.print')
    def test_sympy_equality(self, mock_print):
        try:
            _ = sympy.Symbol('x') == C()
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected assertion error")
        else:
            raise AssertionError("Expected exception")

if __name__ == '__main__':
    unittest.main()
