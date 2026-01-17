 I apologize for the syntax error in the previous response. Here is the corrected standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import *

def test_matrix_product_substitution():
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    expected_latex = "x \\left(-y\\right)"
    actual_latex = latex(expr)
    assert expected_latex == actual_latex, "LaTeX printer omits necessary parentheses in matrix products such as x(-y)"

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        test_matrix_product_substitution()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` if the issue is present and print a stack trace of the issue using the provided `print_stacktrace` function. If the issue is fixed, the script will exit with code 0.