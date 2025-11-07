import sympy as sp
from sympy.abc import m, n

def reproduce_issue():
    result1 = set(sp.diophantine(n**4 + m**4 - 2**4 - 3**4, (m,n), permute=True))
    result2 = set(sp.diophantine(n**4 + m**4 - 2**4 - 3**4, (n,m), permute=True))
    if result1 != {(3, 2)}:
        raise AssertionError("Inconsistent results")
    else:
        print("Results are consistent")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
