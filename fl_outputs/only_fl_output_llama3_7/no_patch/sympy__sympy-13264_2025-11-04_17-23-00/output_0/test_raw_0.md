Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from sympy import symbols, sin, cos, tan, simplify

x, y = symbols('x y')

expr = (sin(x) + cos(y)) * (tan(x) + tan(y))

print("Initial expression:")
print(expr)

simplified_expr1 = simplify(expr)
print("\nAfter first simplify:")
print(simplified_expr1)

simplified_expr2 = simplify(simplified_expr1)
print("\nAfter second simplify:")
print(simplified_expr2)

assert simplified_expr1 == simplified_expr2, "Expected the same result after two simplifications"

try:
    print_stacktrace(AssertionError("Issue not reproduced"))
except AssertionError as e:
    print_stacktrace(e)
```

This script reproduces the issue by first defining an expression `expr` using sympy's symbols and mathematical functions. It then applies `simplify` twice to the expression, printing the results each time. Finally, it asserts that the two simplified expressions are equal, which should raise an `AssertionError` if the issue is present.

If you run this script with Python 3.5.1 and sympy 0.7.6.1, it should print the initial expression, followed by the results of the two simplifications, and then raise an `AssertionError` because the two simplified expressions are not equal.