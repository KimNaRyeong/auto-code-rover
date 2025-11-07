import sympy as sp
from io import StringIO
import sys
import traceback

def diophantine(eq, syms, permute):
    return sp.solve(eq, *syms, simplify=False, permutations=permute)

def print_stacktrace(e: Exception):
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
        result1 = str(diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m,n), permute=True))
        result2 = str(diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n,m), permute=True))
        assert result1 == result2
    except AssertionError:
        print_stacktrace(sys.exc_info()[1])
        sys.exit(1)

if __name__ == "__main__":
    n = sp.symbols('n')
    m = sp.symbols('m')
    reproduce_issue()
