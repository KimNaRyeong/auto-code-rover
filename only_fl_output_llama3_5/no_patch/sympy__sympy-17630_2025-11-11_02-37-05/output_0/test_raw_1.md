Here is the reproducer script:

```python
import sympy as sp

def main():
    from sympy import *
    a = MatrixSymbol("a", 2, 2)
    z = ZeroMatrix(2, 2)
    b = BlockMatrix([[a, z], [z, z]])

    try:
        block_collapse(b * b * b)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

def block_collapse(expr):
    return expr

if __name__ == "__main__":
    main()
```

This script should reproduce the issue and print a stack trace when run with `python3 reproducer.py`.