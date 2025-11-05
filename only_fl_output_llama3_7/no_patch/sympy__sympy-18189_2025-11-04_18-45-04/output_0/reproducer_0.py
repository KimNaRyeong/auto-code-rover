import sympy as sp
from sympy.abc import m, n

def diophantine_expr():
    return n**4 + m**4 - 2**4 - 3**4

def reproduce_issue():
    try:
        result1 = set(sp.diophantine(diophantine_expr(), syms=(m,n), permute=True))
        result2 = set(sp.diophantine(diophantine_expr(), syms=(n,m), permute=True))
        if len(result1) != 8 or result1 != result2:
            raise AssertionError("Inconsistent results")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
