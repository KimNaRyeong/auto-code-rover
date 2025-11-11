import sympy as sp

def reproducer():
    i = sp.symbols('i', integer=True)
    assert sp.Mod(3*i, 2) == sp.Mod(i, 2)

try:
    reproducer()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    exit(0)
