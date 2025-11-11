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

        if str(result1) != str(result2) or str(result1) != str(result3):
            raise AssertionError("Matrix expressions aren't simplified properly")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will run the given matrix operations and check if the results are simplified correctly. If not, it will print a stack trace of the issue and exit with code 1.