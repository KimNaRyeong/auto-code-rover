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
    try:
        import numpy as np
        from sympy import MatrixSymbol, lambdify
        
        X0 = MatrixSymbol('X0', 2, 2)
        # Original incorrect shape 4x4, causing issue because of mismatch with MatrixSymbol shape
        xx = np.random.rand(2, 2)  # Corrected matrix size to match X0
        # Inversion using numpy to ensure operations on `xx` work outside Sympy
        np.linalg.inv(xx)

        X0Inv = X0**-1
        symInv = lambdify(X0, X0Inv, 'numpy')  # Specifying 'numpy' for module
        result = symInv(xx)

        # If the statement below executes without errors, then the issue is fixed/not present.
        print("Issue not detected or already fixed.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is reproducible.")

if __name__ == "__main__":
    main()
