I apologize for the mistake earlier. Here is a new reproducer script that should reproduce the issue:

```python
import sympy as sp

def main():
    from sympy import MatrixSymbol, ZeroMatrix, BlockMatrix

    a = sp.MatrixSymbol("a", 2, 2)
    z = sp.ZeroMatrix(2, 2)
    b = sp.BlockMatrix([[a, z], [z, z]])

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

This script should reproduce the issue and print a stack trace.