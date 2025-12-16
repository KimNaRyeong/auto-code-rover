 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import MatrixSymbol, ZeroMatrix, S, simplify, expand
from sympy.abc import m, n
from sympy.matrices import Matrix
from sympy.printing.str import sstr
from reproducer import print_stacktrace

def test_matrix_expressions_simplification():
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    # Issue reproduction
    expr = -(-A + B) - A + B
    expected_simplified = -(-A + B) - A + B
    expected_expanded = -B + A -A + B

    simplified = simplify(expr)
    expanded = expand(expr)

    assert simplified != expected_simplified, "Matrix expressions aren't simplified properly"
    assert expanded != expected_expanded, "Matrix expressions aren't expanded properly"

    print("Matrix expressions simplification and expansion are working as expected.")

def main():
    try:
        test_matrix_expressions_simplification()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script defines a function `test_matrix_expressions_simplification()` that reproduces the issue by creating matrices `A`, `B`, and `Z`, and then performing simplification and expansion operations on the expression `-(-A + B) - A + B`. If the simplification or expansion results are not as expected, the function raises an `AssertionError`, which is caught by the `main()` function and passed to the `print_stacktrace()` function to print the stack trace. The script exits with code 1 if the issue is present, and 0 if the issue is fixed.