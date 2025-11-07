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
