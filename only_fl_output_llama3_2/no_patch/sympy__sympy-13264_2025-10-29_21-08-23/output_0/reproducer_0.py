import sympy as sp
from sympy import symbols, sin, cos, tan, simplify

x, y = symbols('x y')

expr = (sin(x) + cos(y)) * (tan(x) + tan(y))
print("Initial expression:")
print(expr)

simplified_expr1 = simplify(expr)
print("\nAfter first call to simplify:")
print(simplified_expr1)

simplified_expr2 = simplify(simplified_expr1)
print("\nAfter second call to simplify:")
print(simplified_expr2)

assert simplified_expr1 == simplified_expr2, "Simplify doesn't do the last simplification step"

try:
    raise AssertionError("Expected expressions to be equal")
except AssertionError as e:
    print_stacktrace(e)
