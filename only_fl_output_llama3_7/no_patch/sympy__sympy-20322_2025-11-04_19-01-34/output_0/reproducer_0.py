import sympy
from sympy import ceiling, simplify
import unittest
from io import StringIO
from contextlib import redirect_stdout
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

class TestSympifySimplifyCeiling(unittest.TestCase):

    def test_sympify_simplify_ceiling(self):
        sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False)
        sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True)

        f = StringIO()
        with redirect_stdout(f):
            try:
                result1 = simplify(sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False))
                result2 = simplify(sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True))
                if result1 != result2:
                    raise AssertionError("Inconsistent behavior for sympify/simplify with ceiling")
            except Exception as e:
                print_stacktrace(e)
                sys.exit(1)

if __name__ == '__main__':
    unittest.main()
