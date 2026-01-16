from sympy import *
from sympy.printing.pretty.pretty import PrettyPrinter
from sympy.printing.latex import LatexPrinter

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

def check_printing(expr):
    """
    Checks the string, pretty, and latex representations of an expression.
    Raises an AssertionError if the representation does not match expected behavior.
    """
    expected_pretty = "-B + -A⋅B + A"
    expected_latex = "- B - A B + A"

    str_result = str(expr)
    pretty_result = PrettyPrinter().doprint(expr)
    latex_result = LatexPrinter().doprint(expr)

    try:
        assert str_result == expected_pretty, "str representation mismatch"
        assert pretty_result == expected_pretty, "pretty representation mismatch"
        assert latex_result == expected_latex, "latex representation mismatch"
        print("Issue is fixed. Exiting with code 0.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def main():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    expression = A - A*B - B

    check_printing(expression)

if __name__ == "__main__":
    main()
