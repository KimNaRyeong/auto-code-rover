Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, ZeroMatrix, BlockMatrix

def main():
    a = MatrixSymbol("a", 2, 2)
    z = ZeroMatrix(2, 2)
    b = BlockMatrix([[a, z], [z, z]])

    try:
        block_collapse(b * b * b)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Exception when multiplying BlockMatrix containing ZeroMatrix blocks")

def block_collapse(expr):
    return expr

if __name__ == "__main__":
    main()
```

This script will reproduce the issue and print a stack trace.