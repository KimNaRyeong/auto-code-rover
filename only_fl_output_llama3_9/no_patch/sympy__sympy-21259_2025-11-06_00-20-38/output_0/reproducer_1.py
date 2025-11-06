import sympy as sp
from sympy.core import Eq, Mod

def test_as_relational():
    x = 5  # This variable will be used in the Range object
    try:
        range_obj = sp.Range(3, 11, 2)
        result = range_obj.as_relational(x)
        assert False, "Expected AssertionError"
    except AssertionError:
        print_stacktrace(sys.exc_info()[1])

if __name__ == "__main__":
    test_as_relational()
