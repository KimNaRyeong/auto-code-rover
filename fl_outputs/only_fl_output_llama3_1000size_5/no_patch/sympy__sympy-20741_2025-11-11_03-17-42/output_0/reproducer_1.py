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

def main():
    m = 2
    n = 3
    A = sp.MatrixSymbol('A', m, n)
    B = sp.MatrixSymbol('B', m, n)
    Z = sp.ZeroMatrix(m, n)

    try:
        result1 = -(-A + B) - A + B
        result2 = (-(-A + B) - A + B).simplify()
        result3 = (-(-A + B) - A + B - Z).simplify()

        if result1 != -B + sp.MatrixSymbol('A', m, n) - sp.MatrixSymbol('A', m, n) + B or \
           result2 != result1 or \
           result3 != -B + sp.MatrixSymbol('A', m, n) - sp.MatrixSymbol('A', m, n) + B:
            raise AssertionError("Matrix expressions aren't simplified properly")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
