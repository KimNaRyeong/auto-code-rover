 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import MatrixSymbol, ZeroMatrix, S, simplify, expand
from sympy.abc import m, n
from sympy.matrices import Matrix
from sympy.simplify.simplify import nsimplify

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    m = S(3)
    n = S(4)

    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    # Issue reproduction
    expr = -(-A + B) - A + B
    expected_expanded = Matrix(-B + A - A + B)
    actual_expanded = expand(expr)
    assert expected_expanded == actual_expanded, "Matrix expressions aren't expanded properly"

    expected_simplified = Matrix(-B + A - A + B)
    actual_simplified = simplify(expr)
    assert expected_simplified == actual_simplified, "Matrix expressions aren't simplified properly"

    # Adding zero matrix should not affect the result
    expr_with_zero = expr - Z
    expected_expanded_with_zero = Matrix(-B + A - A + B)
    actual_expanded_with_zero = expand(expr_with_zero)
    assert expected_expanded_with_zero == actual_expanded_with_zero, "Adding zero matrix doesn't work properly"

    expected_simplified_with_zero = Matrix(-B + A - A + B)
    actual_simplified_with_zero = simplify(expr_with_zero)
    assert expected_simplified_with_zero == actual_simplified_with_zero, "Adding zero matrix doesn't work properly"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script reproduces the issue and raises an `AssertionError` when executed with `python3 reproducer.py`. The script prints a stack trace of the issue.