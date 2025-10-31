import sympy as sp
from unittest import TestCase

class TestAsRelational(TestCase):
    def test_as_relational(self):
        try:
            range_obj = sp.Range(3, 11, 2)
            range_obj.as_relational(x=1)
        except AssertionError:
            print_stacktrace(sys.exc_info()[1])
            raise
        else:
            self.fail("Expected AssertionError")

if __name__ == "__main__":
    test_as_relational = TestAsRelational()
    test_as_relational.test_as_relational()
