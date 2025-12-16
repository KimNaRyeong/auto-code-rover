 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import *
from reproducer import print_stacktrace

def test_issue():
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    expected_latex = "x \\left(-y\\right)"
    actual_latex = latex(expr)
    assert actual_latex == expected_latex, f"Actual LaTeX output: {actual_latex}"

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
The `test_issue` function creates two matrix symbols `x` and `y`, calculates the product of `x` and `y` and substitutes `y` with `-y`. It then compares the expected LaTeX output with the actual LaTeX output and raises an `AssertionError` if they are not equal.

The `print_stacktrace` function is defined in the `reproducer` module and is used to print the stack trace when the `AssertionError` is raised.

When the script is executed with `python3 reproducer.py`, it will print the stack trace and exit with code 1 if the issue is present, and exit with code 0 if the issue is fixed.