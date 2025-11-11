Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):

    def test_matrix_expression_simplification(self):
        m = 2
        n = 3
        from sympy.abc import A, B
        from sympy.matrices.expressions import ZeroMatrix, MatrixSymbol
        A = MatrixSymbol('A', m, n)
        B = MatrixSymbol('B', m, n)
        Z = ZeroMatrix(m, n)

        result1 = (-(-A + B) - A + B).simplify()
        result2 = (-(-A + B) - A + B - Z).simplify()

        if result1 != -A + B or result2 != -A + B:
            raise AssertionError("Matrix expressions aren't simplified properly")

if __name__ == "__main__":
    try:
        Reproducer().test_matrix_expression_simplification()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue is fixed")
        exit(0)

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