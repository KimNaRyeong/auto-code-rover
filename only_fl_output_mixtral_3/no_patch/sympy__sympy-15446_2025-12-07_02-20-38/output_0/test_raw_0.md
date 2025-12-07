 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import *
from reproducer import print_stacktrace

def test_matrix_product_substitution():
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    expected_latex = "x \\left(-y\\right)"
    actual_latex = latex(expr)
    assert expected_latex == actual_latex, "LaTeX printer omits necessary parentheses in matrix products such as x(-y)"

if __name__ == "__main__":
    test_matrix_product_substitution()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` if the issue is present and print a stack trace of the issue using the provided `print_stacktrace` function. If the issue is fixed, the script will exit with code 0.