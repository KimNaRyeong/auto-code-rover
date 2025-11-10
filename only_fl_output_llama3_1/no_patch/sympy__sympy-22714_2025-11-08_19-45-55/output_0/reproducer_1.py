import sympy as sp
from unittest import TestCase

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

class Reproducer(TestCase):
    def test_issue(self):
        try:
            with sp.evaluate(False):
                sp.S('Point2D(Integer(1),Integer(2))')
            self.fail("Expected ValueError")
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue not present")

if __name__ == "__main__":
    Reproducer().test_issue()
