Here is the reproducer script:

```python
import sympy as sp
from sympy import I, MatrixSymbol

def main():
    M = MatrixSymbol('M', 2, 2)
    try:
        print(I * M)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError"

if __name__ == "__main__":
    main()
```

This script creates a `MatrixSymbol` and then tries to multiply it with the imaginary unit `I`. If the issue is present, an `AssertionError` will be raised when trying to run this script.