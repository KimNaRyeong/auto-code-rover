 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy as sp
from pprint import pprint

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

a = t44("a")
b = t44("b")

e = a * b
e2 = sub_in_matrixsymbols(e, [sp.MatrixSymbol("a", 4, 4), sp.MatrixSymbol("b", 4, 4)])
cse_subs, cse_reduced = sp.cse(e2)

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    assert not cse_reduced.free_symbols, "MatrixSymbols are not fully eliminated by cse!"
except AssertionError as e:
    print_stacktrace(e)
    raise
```
This script defines the `sub_in_matrixsymbols` and `t44` functions, creates the matrices `a` and `b`, and constructs the expression `e`. It then substitutes `MatrixSymbol`s for the matrix elements in `e` and applies the `cse` function. The script checks if the resulting expression `cse_reduced` contains any `MatrixSymbol`s, and raises an `AssertionError` if it does. The `print_stacktrace` function is used to print the stack trace when the assertion fails.

To run the script, save it as `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.