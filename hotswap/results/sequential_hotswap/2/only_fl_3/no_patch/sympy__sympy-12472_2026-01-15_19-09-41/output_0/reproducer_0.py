from sympy import sqrt, I, simplify
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

def test_sqrt_issue():
    try:
        # The expression that is expected to cause an issue according to the description.
        expr = sqrt((3 + 4*I)/(3 - 4*I))
        simp_expr = simplify(expr)  # Attempt to simplify the expression to trigger the issue
        # Check if the issue is present by verifying the expression does not match the expected correct form.
        # Please note: The exact condition may need adjusting based on the specific nature of the bug and the expected fix.
        assert simp_expr != sqrt(-1/(3 - 4*I))*sqrt(-3 - 4*I), "Unexpected factorization of sqrt"
        print("Issue not found, possibly fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code to indicate the presence of the issue.

if __name__ == "__main__":
    test_sqrt_issue()
    sys.exit(0)  # Exit successfully if no error was raised.
