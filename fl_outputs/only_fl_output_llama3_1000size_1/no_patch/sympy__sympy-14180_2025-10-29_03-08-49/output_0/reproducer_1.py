import math
from sympy import latex, ln

def reproduce_issue():
    try:
        converted_expression = latex(ln(10))
        assert "ln" in converted_expression, "Expected 'ln' but got: " + converted_expression
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
