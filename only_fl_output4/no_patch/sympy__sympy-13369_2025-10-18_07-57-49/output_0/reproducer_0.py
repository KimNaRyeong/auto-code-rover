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

def test_symbolic_eigenvals():
    x = Symbol('x')
    lam = Symbol('lambda')
    M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])
    try:
        eigenvals = M.eigenvals()
        assert eigenvals, "Eigenvalues should not be empty"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected eigenvalues could not be computed using .eigenvals method")

    # Testing if the roots can be computed separately as a workaround
    roots_of_charpoly = solve(det(lam * eye(3) - M), lam)
    try:
        assert roots_of_charpoly, "Roots of characteristic polynomial should not be empty"
    except AssertionError:
        print("Failed to find roots using workaround with solve(det(lam*eye(3)-M), lam)")
        raise

    try:
        charpoly_roots = roots(M.charpoly(lam))
        assert charpoly_roots, "Roots of charpoly should not be empty"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected roots could not be computed using roots(M.charpoly())")

if __name__ == "__main__":
    test_symbolic_eigenvals()
    print("If this message is printed, the issue is not present.")
