import sympy as sp
from sympy import latex

def main():
    expr = sp.ln(10)
    latex_expr = latex(expr)

    expected_latex = r'\ln\left(10\right)'
    assert latex_expr == expected_latex, f"Expected {expected_latex} but got {latex_expr}"

try:
    main()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
