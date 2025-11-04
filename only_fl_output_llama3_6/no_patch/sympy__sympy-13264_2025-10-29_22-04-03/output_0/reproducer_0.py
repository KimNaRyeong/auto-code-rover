import sympy as sp
from sympy import symbols, sin, cos, tan, simplify

x, y = symbols('x y')

expr = (sin(x)**2 + cos(x)**2) * (1 + 2*tan(y)**2)

print("Initial expression:")
print(expr)

initial_ops = len(str(expr).replace('**', '^').replace('*', ' ').split())
print(f"Initial operations: {initial_ops}")

simplified_expr = simplify(expr)
print("\nSimplified expression after first call to simplify:")
print(simplified_expr)

simplified_ops = len(str(simplified_expr).replace('**', '^').replace('*', ' ').split())
print(f"Simplified operations: {simplified_ops}")

assert simplified_ops < initial_ops, "Expected fewer operations in the simplified expression"

try:
    double_simplified_expr = simplify(simplified_expr)
    print("\nSimplified expression after second call to simplify:")
    print(double_simplified_expr)

    double_simplified_ops = len(str(double_simplified_expr).replace('**', '^').replace('*', ' ').split())
    print(f"Simplified operations: {double_simplified_ops}")

    assert double_simplified_ops < simplified_ops, "Expected fewer operations in the simplified expression"
except AssertionError as e:
    print_stacktrace(e)
    raise
