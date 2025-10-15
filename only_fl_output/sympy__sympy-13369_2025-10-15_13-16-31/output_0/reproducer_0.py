# reproducer.py
from sympy import Symbol, Matrix, exp, solve, det, eye

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
        x = Symbol('x')
        M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])
        eigenvals_result = M.eigenvals()
        # If no exception raised, we consider the issue fixed
        if not eigenvals_result:
            raise AssertionError("Eigenvals method returned an empty result.")

        # Additional check to ensure the roots method also works as expected,
        # which was part of the original issue.
        lam = Symbol('lambda')
        roots_solution = solve(det(lam * eye(3) - M), lam)
        # assert that roots_solution is not empty, this was the root cause of the issue
        assert roots_solution, "Failed to find roots using solve(det(lam*eye(3) - M), lam)"
        print("Issue seems fixed, eigenvals method returned results")
    except Exception as e:
        print_stacktrace(e)
        # If you encounter the specific error mentioned, change the raise to assert to reflect the issue reproduction
        if "Could not compute eigenvalues" in str(e):
            assert False, "The issue is present."
        else:
            # If the issue is not reproduced but another error occurred, let's not fail the test
            print("An unexpected error occurred, which does not directly indicate the original issue is still present.")
        raise

if __name__ == "__main__":
    main()
