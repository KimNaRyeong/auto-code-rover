Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, ZeroMatrix, BlockMatrix

def main():
    a = sp.MatrixSymbol("a", 2, 2)
    z = sp.ZeroMatrix(2, 2)
    b = sp.BlockMatrix([[a, z], [z, z]])

    try:
        block_collapse(b * b * b)
    except Exception as e:
        print_stacktrace(e)
        raise

def block_collapse(expr):
    result = expr
    while True:
        if isinstance(result, (sp.Matrix, sp.BlockMatrix)):
            rule = sp.strategies.core.exhaustive_rl
            new, old = rule(result), result
            if new != old:
                result = new
            else:
                break
        elif isinstance(result, sp.Zero):
            raise AssertionError("Exception when multiplying BlockMatrix containing ZeroMatrix blocks")
        else:
            break

if __name__ == "__main__":
    main()
```

This script will reproduce the issue when run with `python3 reproducer.py`.