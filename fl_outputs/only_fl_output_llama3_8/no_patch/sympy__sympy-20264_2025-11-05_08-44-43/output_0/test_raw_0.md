Here is the reproducer script:

```python
import sympy as sp
from sympy import Rational, Pow

def main():
    try:
        latex_expr = Pow(Rational(1, 2), -1, evaluate=False)
        print(latex(latex_expr))
    except RecursionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script attempts to convert the expression `Pow(Rational(1, 2), -1)` to LaTeX using sympy's `latex` function. If a `RecursionError` is raised during this process, it prints the stack trace of the error.