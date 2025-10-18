```python
import sympy as sp
import sys

def print_stacktrace(e: Exception):
    import traceback
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
    try:
        a = t44("a")
        b = t44("b")

        e = a * b

        e2 = sub_in_matrixsymbols(e, [sp.MatrixSymbol("a", 4, 4), sp.MatrixSymbol("b", 4, 4)])
        cse_subs, cse_reduced = sp.cse(e2)

        expected_substitutions = [sp.MatrixSymbol("a", 4, 4), sp.MatrixSymbol("b", 4, 4)]
        for sym, expr in cse_subs:
            if isinstance(expr, sp.MatrixSymbol) and expr not in expected_substitutions:
                raise AssertionError(f"Unexpected matrix symbol substitution: {expr}")

        # If there's no error, we print a success message
        print("No issue detected with cse() for MatrixSymbol indexing.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```