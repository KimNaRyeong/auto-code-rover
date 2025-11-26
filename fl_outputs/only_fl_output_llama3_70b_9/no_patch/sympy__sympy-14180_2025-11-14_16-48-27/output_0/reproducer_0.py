import sympy as sp
from sympy import latex

def test_latex_conversion():
    expr = sp.ln(10)
    latex_expr = latex(expr)
    expected_latex = r'\ln\left(10\right)'
    assert latex_expr == expected_latex, f"Expected {expected_latex} but got {latex_expr}"

def main():
    try:
        test_latex_conversion()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
