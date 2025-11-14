Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from reproducer import print_stacktrace

def main():
    m = 2
    n = 3
    A = sp.MatrixSymbol('A', m, n)
    B = sp.MatrixSymbol('B', m, n)
    Z = sp.ZeroMatrix(m, n)

    try:
        result1 = -(-A + B) - A + B
        result2 = (-(-A + B) - A + B).simplify()
        result3 = (-(-A + B) - A + B - Z).simplify()

        if str(result1) != "-B + A -A + B" or \
           str(result2) != "B + A -A + B" or \
           str(result3) != "B + A -A + B":
            raise AssertionError("Matrix expressions aren't simplified properly")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will run the given matrix operations and check if the results are correct. If not, it will print a stack trace of the issue and exit with code 0 when the issue is fixed.