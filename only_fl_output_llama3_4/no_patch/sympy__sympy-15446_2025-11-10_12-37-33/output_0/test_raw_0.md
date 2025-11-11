Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, latex

def main():
    x = sp.MatrixSymbol('x', 2, 2)
    y = sp.MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    expected_latex = r'$\left(\begin{array}{cc}x_{00}&x_{01}\\x_{10}&x_{11}\end{array}\right)\left(\begin{array}{cc}-y_{00}&-y_{01}\\-y_{10}&-y_{11}\end{array}\right)$'
    actual_latex = latex(expr)
    if expected_latex != actual_latex:
        raise AssertionError("LaTeX printer omits necessary parentheses in matrix products")

try:
    main()
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script will run the original code and compare the expected LaTeX output with the actual one. If they don't match, it will raise an `AssertionError` and print a stack trace using the provided function.