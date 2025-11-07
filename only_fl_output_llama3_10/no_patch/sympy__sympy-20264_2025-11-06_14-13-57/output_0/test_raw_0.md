Here is the reproducer script:

```python
import sympy as sp

def main():
    try:
        expr = sp.Pow(sp.Rational(1, 2), -1, evaluate=False)
        latex_expr = str(sp.latex(expr))
        print(latex_expr)
    except RecursionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script creates a `Pow` expression with a rational number and an exponent of -1, then attempts to convert it to LaTeX. If the conversion raises a `RecursionError`, the script prints the stack trace using the provided function.