from sympy import symbols, sin

x = symbols('x')

def arg(y):
    return y

try:
    assert arg(sin(x)).is_real == True
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully")
exit(0)
