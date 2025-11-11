Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, ZeroMatrix

def main():
    m = 2
    n = 3
    A = sp.MatrixSymbol('A', m, n)
    B = sp.MatrixSymbol('B', m, n)
    Z = sp.ZeroMatrix(m, n)

    try:
        result1 = -(-A + B) - A + B
        if str(result1) != "-B + A":
            raise AssertionError("Matrix expressions aren't simplified properly")
        
        result2 = (-(-A + B) - A + B).simplify()
        if str(result2) != "-B + A":
            print_stacktrace(AssertionError("Matrix expressions aren't simplified properly"))
            exit(1)
        
        result3 = (-(-A + B) - A + B - Z).simplify()
        if str(result3) != "-B + A":
            print_stacktrace(AssertionError("Matrix expressions aren't simplified properly"))
            exit(1)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will run the given matrix operations and check if the results are simplified correctly. If not, it will raise an `AssertionError` with a stack trace of the issue and exit with code 1.