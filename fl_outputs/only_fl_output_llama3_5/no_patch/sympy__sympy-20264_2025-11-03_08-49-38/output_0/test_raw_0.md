Here is the reproducer script:

```python
import sympy as sp
from sympy import Rational, Pow

def reproduce_issue():
    try:
        latex_expr = Pow(Rational(1, 2), -1, evaluate=False)
        print(latex_expr)
    except RecursionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to convert the expression `Pow(Rational(1, 2), -1, evaluate=False)` to LaTeX using sympy's `latex` function. If an error occurs during this process (i.e., a RecursionError is raised), it will print the stack trace of the error.