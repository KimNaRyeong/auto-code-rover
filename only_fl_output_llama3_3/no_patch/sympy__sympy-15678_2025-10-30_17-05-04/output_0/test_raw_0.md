Here is the reproducer script `reproducer.py`:

```python
import sympy as sp
from reproducer import print_stacktrace

def main():
    try:
        idiff(sp.Eq(sp.exp(sp.sympify('y')) * sp.sympify('y'), sp.sympify('x') * sp.exp(sp.sympify('x'))), sp.sympify('y'), sp.sympify('x'))
        idiff(sp.sympify('f(x)*exp(f(x)) - x*exp(x)'), sp.sympify('f(x)'), sp.sympify('x'))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exceptions not raised")

if __name__ == "__main__":
    main()
```

This script tries to reproduce the issue by calling `idiff` with different inputs. If any of these calls raise an exception, it prints the stack trace and raises an `AssertionError`.