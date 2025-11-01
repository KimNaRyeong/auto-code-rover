import sympy as sp
from sympy import Mod, Symbol

def reproduce_issue():
    i = Symbol('i', integer=True)

    try:
        assert Mod(3*i, 2) == Mod(i, 2)
    except AssertionError:
        print_stacktrace(sys.exc_info()[1])
        exit(0)
    else:
        raise Exception("Issue not found")
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
