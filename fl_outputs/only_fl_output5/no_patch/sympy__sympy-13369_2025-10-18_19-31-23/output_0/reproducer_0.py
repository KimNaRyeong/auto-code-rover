from sympy import *
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

def main():
    x = Symbol('x')
    M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])

    try:
        # Attempt to get eigenvalues
        eigenval_result = M.eigenvals()
    except Exception as e:
        print("Error found while finding eigenvalues with .eigenvals()")
        print_stacktrace(e)
    else:
        assert eigenval_result, "No eigenvalue found"

    lam = Symbol('lambda')
    try:
        # Attempt to solve characteristic polynomial
        roots_result = solve(det(lam*eye(3) - M), lam)
        assert roots_result, "No root found"
    except AssertionError as e:
        print("Error while solving characteristic polynomial directly.")
        print_stacktrace(e)
        sys.exit(1)

    try:
        # Check consistency with roots of charpoly
        roots_charpoly_result = roots(M.charpoly())
        assert roots_charpoly_result, "Roots of charpoly() returned empty"
    except Exception as e:
        print("Error with roots(M.charpoly())")
        print_stacktrace(e)
        sys.exit(1)

    print("All tests passed successfully.")

if __name__ == "__main__":
    main()
