import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.function import Function

def test_reproducer():
    try:
        factorial = Function('factorial')
        result = factorial()
        assert result == 1, "Factorial should return 1 for no argument"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Test failed")

if __name__ == "__main__":
    test_reproducer()
