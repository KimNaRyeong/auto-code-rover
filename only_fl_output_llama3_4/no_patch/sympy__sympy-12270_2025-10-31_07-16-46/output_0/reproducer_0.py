import sympy as sp
from sympy import Mul, I

def main():
    x = sp.symbols('x')
    y = sp.symbols('y')

    # Reproduce the first bug
    try:
        result = (-2*x - 4*y - 8).extract_multiplicatively(-2)
        assert False, "Expected ValueError"
    except Exception as e:
        print_stacktrace(e)

    # Reproduce the second bug
    try:
        result = (2*x + 4*y + 8).extract_multiplicatively(-2)
        assert False, "Expected ValueError"
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
