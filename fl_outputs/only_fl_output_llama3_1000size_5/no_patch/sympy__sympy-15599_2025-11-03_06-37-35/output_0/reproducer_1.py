import sympy as sp

def reproducer():
    i = 3
    assert sp.Mod(i, 2) != sp.Mod(i/3, 2)

try:
    reproducer()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
