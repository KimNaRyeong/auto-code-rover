```python
import sympy as sp
from pprint import pprint

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

def sub_in_matrixsymbols(exp, matrices):
    for matrix in matrices:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                name = "%s_%d_%d" % (matrix.name, i, j)
                sym = sp.symbols(name)
                exp = exp.subs(sym, matrix[i, j])
    return exp

def t44(name):
    return sp.Matrix(4, 4, lambda i, j: sp.symbols('%s_%d_%d' % (name, i, j)))

def test_issue():
    # Construct matrices of symbols
    a = t44("a")
    b = t44("b")

    # Set up expression
    e = a * b

    # Replace symbols with MatrixSymbols
    e2 = sub_in_matrixsymbols(e, [sp.MatrixSymbol("a", 4, 4), sp.MatrixSymbol("b", 4, 4)])
    cse_subs, cse_reduced = sp.cse(e2)

    # Attempt to reproduce the issue: 'x0' and 'x2' are just copies of 'a' and 'b'
    for sym, expr in cse_subs:
        if isinstance(expr, sp.MatrixElement) and expr.args[0].is_MatrixSymbol:
            raise AssertionError("MatrixSymbol indexing leads to unexpected behavior: {}".format(expr))

    print("Issue not present.")

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
```