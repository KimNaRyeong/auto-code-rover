import sympy as sp
from sympy import symbols, Mod

def reproducer():
    i = symbols('i', integer=True)
    assert Mod(3*i, 2) != Mod(i, 2), "Mod(3*i, 2) should not be simplified to Mod(i, 2)"
    print_stacktrace(AssertionError("Expected Mod(3*i, 2) not to be simplified"))

if __name__ == "__main__":
    reproducer()
