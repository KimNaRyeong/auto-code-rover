Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from sympy import I, Mul

def extract_multiplicatively(expr, value):
    try:
        return expr.extract_multiplicatively(value)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected multiplicatively extraction to work")

sp.init_printing(use_latex=True)

x = sp.symbols('x')
y = sp.symbols('y')

expr1 = -2*x - 4*I
print(expr1.extract_multiplicatively(-2))

expr2 = -2*x - 4*y - 8
print(expr2.extract_multiplicatively(2))
print(expr2.extract_multiplicatively(-1))
try:
    print(expr2.extract_multiplicatively(-2))
except Exception as e:
    raise AssertionError("Expected multiplicatively extraction to work")

if __name__ == "__main__":
    pass
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.