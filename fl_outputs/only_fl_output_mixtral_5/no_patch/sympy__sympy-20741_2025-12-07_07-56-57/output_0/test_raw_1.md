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
    assert expand(matrix_expr) != expand(-(-A + B) - A + B)
    assert simplify(matrix_expr) != simplify(-(-A + B) - A + B)
    assert expand(matrix_expr - Z) != expand(-(-A + B) - A + B - Z)
    assert simplify(matrix_expr - Z) != simplify(-(-A + B) - A + B - Z)
except Exception as e:
    print_stacktrace(e)
else:
    print("No issue found.")
    raise AssertionError("Issue not reproduced.")
```

When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.