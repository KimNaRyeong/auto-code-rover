Below is a `reproducer.py` Python script that follows your specifications. This script will run and reproduce the described issue, raising an `AssertionError` if the problem is present. It also includes the `print_stacktrace` function for printing stack traces with clear line numbers.

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

def main():
    # Construct matrices of symbols
    a = t44("a")
    b = t44("b")

    # Set up expression
    e = a * b

    # Replace with MatrixSymbols
    e2 = sub_in_matrixsymbols(e, [sp.MatrixSymbol("a", 4, 4), sp.MatrixSymbol("b", 4, 4)])

    cse_subs, cse_reduced = sp.cse(e2)

    assert len(cse_subs) > 0, "Expected some common subexpressions but got none."

    all_subs_involved = all(isinstance(expr, sp.MatrixElement) for sym, expr in cse_subs if isinstance(sym, sp.Symbol))

    # The issue is present if not all substitutions involve MatrixElement.
    if not all_subs_involved:
        raise AssertionError("Not all substitutions involve MatrixElement. Issue present.")

if __name__ == "__main__":
    try:
        main()
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
```

This script performs the calculations using SymPy to identify the problem described with `MatrixSymbol` indexing during common subexpression elimination (CSE). If the issue occurs, it will raise an `AssertionError` and print the stack trace. If the issue is fixed, it simply exits with code 0.