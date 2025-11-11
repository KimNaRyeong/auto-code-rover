Here is the reproducer script:

```python
import sympy as sp
from sympy import latex, MatrixSymbol

def main():
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    expected_latex = r"x\left(-y\right)"
    actual_latex = latex(expr)
    
    if actual_latex != expected_latex:
        raise AssertionError("LaTeX printer omits necessary parentheses in matrix products")
    else:
        print("Issue fixed")

try:
    main()
except Exception as e:
    print_stacktrace(e)
    exit(1)

```

You can run this script by executing `python3 reproducer.py` in the root directory of your project.