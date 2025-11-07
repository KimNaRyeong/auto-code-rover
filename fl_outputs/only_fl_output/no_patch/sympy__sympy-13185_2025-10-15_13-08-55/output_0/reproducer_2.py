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
                name = f"{matrix.name}_{i}_{j}"
                sym = sp.symbols(name)
                exp = exp.subs(sym, matrix[i, j])
    return exp

def main():
    # Create symbols for testing
    a = sp.MatrixSymbol('a', 4, 4)
    b = sp.MatrixSymbol('b', 4, 4)
    expr = a*b

    # Substitute symbols with their indexed counterparts
    expr_subbed = sub_in_matrixsymbols(expr, [a, b])

    # Perform common subexpression elimination
    cse_subs, cse_reduced = sp.cse(expr_subbed)

    # Here the issue checker code would go
    # For the sake of demonstrative purposes, let's say we're checking if x0 references directly 'a' and is not a copy
    try:
        if not any([s for s in cse_subs if ('x0', 'a') == s]):
            raise AssertionError("Expected substitution from 'a' to 'x0' directly is missing")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code to highlight the issue presence

    # If no issue was found
    print("No issue detected. Exiting normally.")
    sys.exit(0)

if __name__ == "__main__":
    main()
