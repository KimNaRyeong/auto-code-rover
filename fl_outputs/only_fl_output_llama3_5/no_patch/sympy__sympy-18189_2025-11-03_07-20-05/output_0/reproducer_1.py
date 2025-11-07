import sympy as sp
from sympy.abc import m, n

def diophantine(eq, syms, permute):
    if permute:
        return set(sp.solve(eq, *syms))
    else:
        return {tuple(x) for x in sp.solve(eq, *syms)}

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        result1 = diophantine(n**4 + m**4 - 2**4 - 3**4, (m,n), True)
        result2 = diophantine(n**4 + m**4 - 2**4 - 3**4, (n,m), True)
        assert set(result1) == set(result2)
    except AssertionError:
        print_stacktrace(sys.exc_info()[1])
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
