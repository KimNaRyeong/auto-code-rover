import sympy as sp
from sympy.solvers.diophantine import diophantine

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

def main():
    eq = sp.Eq(n**4 + m**4 - 2**4 - 3**4, 0)
    result1 = diophantine(eq, syms=(m,n), permute=True)
    result2 = diophantine(eq, syms=(n,m), permute=True)

    try:
        assert set(result1) == set(result2), "Incomplete results depending on syms order with permute=True"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    m, n = sp.symbols("m n")
    main()
