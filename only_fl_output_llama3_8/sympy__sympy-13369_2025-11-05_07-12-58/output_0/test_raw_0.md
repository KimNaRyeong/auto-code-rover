Here is the reproducer script:

```python
import sympy as sp
from sympy import Symbol, Matrix, eye

def main():
    x = Symbol('x', real=True)
    M = Matrix([[x, 0, 1], [x, 0, 2], [sp.exp(x), 1, 0]])
    try:
        M.eigenvals()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected eigenvalues to be computed")

if __name__ == "__main__":
    main()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and raise an `AssertionError`.