import sympy as sp
from sympy.abc import m, n

def diophantine(equation, syms, permute=True):
    return set(sp.solve(equation, *syms, permutations=permute))

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
        result1 = diophantine(n**4 + m**4 - 2**4 - 3**4, (m,n), permute=True)
        result2 = diophantine(n**4 + m**4 - 2**4 - 3**4, (n,m), permute=True)
        if len(result1) != 8 or len(result2) != 1:
            raise AssertionError("Inconsistent results")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
