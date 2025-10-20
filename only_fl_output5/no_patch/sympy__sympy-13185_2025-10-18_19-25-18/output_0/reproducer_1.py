# reproducer.py
import sympy as sp

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
    try:
        a = t44("a")
        b = t44("b")
        e = a * b
        e2 = sub_in_matrixsymbols(e, [sp.MatrixSymbol("a", 4, 4), sp.MatrixSymbol("b", 4, 4)])
        cse_subs, cse_reduced = sp.cse(e2)

        # Check if `x0` and `x2` are treated as symbolic representations without direct copying
        # of the matrices `a` and `b`. This condition needs to be crafted based on the 
        # original issue description and expected behavior.
        for sym, expr in cse_subs:
            # Check for the direct assignment of MatrixSymbols which indicate the issue.
            if isinstance(expr, sp.MatrixSymbol):
                raise AssertionError("MatrixSymbol indexing results in direct reference copying.")

    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print('Issue is fixed or not reproduced.')
        raise SystemExit(0)

if __name__ == "__main__":
    main()
