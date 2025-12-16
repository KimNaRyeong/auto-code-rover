 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import MatrixSymbol, ZeroMatrix, S, expand, simplify
from sympy.abc import m, n
from sympy.matrices import Matrix

A = MatrixSymbol('A', m, n)
B = MatrixSymbol('B', m, n)
Z = ZeroMatrix(m, n)

matrix_expr = -(-A + B) - A + B

try:
    assert expand(matrix_expr) == -B + A -A + B
    assert simplify(matrix_expr) == matrix_expr
except AssertionError as e:
    print_stacktrace(e)
else:
    print("The issue is not reproduced.")
    exit(0)
```

When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    assert expand(matrix_expr) == -B + A -A + B
AssertionError
```

This indicates that the `expand` method does not simplify the matrix expression as expected.