import sympy as sp
from sympy import symbols, Dummy

def main():
    x = symbols('x')
    y = symbols('y', commutative=False)

    # Create a non-commutative object with commutative free_symbols
    obj = y * x + 1

    try:
        result = sp.factor(obj)
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
