Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from sympy import Symbol, I

def main():
    x = Symbol('x')
    try:
        print(sp.simplify(sp.cos(x)**I))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
```

This script imports the necessary modules, defines a `main` function that reproduces the issue by calling `simplify(cos(x)**I)`, and then prints the stack trace of the exception if it occurs.