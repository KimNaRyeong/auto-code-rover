Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import sympy as sp

def test_latex_conversion():
    expr = sp.Pow(sp.Rational(1, 2), -1, evaluate=False)
    try:
        latex_expr = sp.latex(expr)
        print(latex_expr)  # Should print '\frac{1}{\frac{1}{2}}'
    except RecursionError as e:
        print_stacktrace(e)
        assert False, "RecursionError occurred while converting sympy expression to LaTeX"

def test_latex_conversion_negative():
    expr = sp.Pow(sp.Rational(-1, -5), -1, evaluate=False)
    try:
        latex_expr = sp.latex(expr)
        print(latex_expr)  # Should print '\frac{1}{-\frac{1}{5}}'
    except RecursionError as e:
        print_stacktrace(e)
        assert False, "RecursionError occurred while converting sympy expression to LaTeX"

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

if __name__ == "__main__":
    test_latex_conversion()
    test_latex_conversion_negative()
```
This script defines two functions `test_latex_conversion` and `test_latex_conversion_negative` that attempt to convert sympy expressions to LaTeX using the `latex` function. If a `RecursionError` occurs during the conversion, it prints the stack trace of the error using the `print_stacktrace` function and raises an `AssertionError`.