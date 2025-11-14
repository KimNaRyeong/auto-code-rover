import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def main():
    transformations = (standard_transformations + (implicit_multiplication_application,))
    expr1 = parse_expr('2**n * 3**n')
    expr2 = parse_expr('2**n3**n', transformations=transformations)

    try:
        result = expr1 - expr2
        assert result == 0, "Expected 0 but got {}".format(result)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
