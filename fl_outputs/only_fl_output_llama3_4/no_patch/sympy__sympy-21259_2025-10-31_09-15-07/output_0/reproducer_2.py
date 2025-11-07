import sympy as sp
from sympy import Mod, floor

def test_as_relational():
    x = 5  # This variable should be used in the Range object creation
    try:
        range_obj = sp.Range(3,11,2)
        result = range_obj.as_relational(x)
        if not (result == "(x >= 3) & (x <= 9) & Eq(x, floor(x))"):
            print_stacktrace(AssertionError("Expected relational expression '(x >= 3) & (x <= 9) & Eq(x, floor(x))'"))
            raise
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_as_relational()
