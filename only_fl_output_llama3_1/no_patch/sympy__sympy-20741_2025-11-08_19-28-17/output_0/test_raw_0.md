Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, ZeroMatrix

def main():
    m = 2
    n = 3
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    try:
        result1 = -(-A + B) - A + B
        result2 = (-(-A + B) - A + B).simplify()
        result3 = (-(-A + B) - A + B - Z).simplify()

        if not (result1 == -B + A - A + B and result2 != -B + A - A + B and result3 == -B + A - A + B):
            raise AssertionError("Matrix expressions aren't simplified properly")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will run the given matrix operations, check if the results are correct and simplify the expressions. If any of these operations fail to produce the expected result or simplify the expressions correctly, it will raise an `AssertionError` with a stack trace.