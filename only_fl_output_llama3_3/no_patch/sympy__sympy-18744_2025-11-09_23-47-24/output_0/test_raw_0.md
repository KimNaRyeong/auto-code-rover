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
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
```

You can run this script using `python3 reproducer.py`. If the issue is present, it will print a stack trace and then raise an assertion error.