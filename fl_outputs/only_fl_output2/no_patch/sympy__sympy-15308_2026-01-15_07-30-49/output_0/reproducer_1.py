# reproducer.py
from sympy import MatrixSymbol, latex, trace
from sympy.abc import n

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

def test_latex_printing_for_matrix_expression():
    A = MatrixSymbol("A", n, n)
    latex_result = latex(trace(A**2))
    expected_latex = 'Trace(A^2)' # This is the incorrect current behavior that should be checked against
    try:
        # The assertion checks if the issue still exists (i.e., if the latex output is wrong).
        assert latex_result == expected_latex, f"Expected {expected_latex}, but got {latex_result}"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with a non-zero exit code to indicate failure

def main():
    try:
        test_latex_printing_for_matrix_expression()
    except SystemExit as e:
        # In case of system exit with failure, just pass to allow the printout of the issue.
        pass
    else:
        print("Issue appears to be fixed.")  # No AssertionError caught means the output was as expected (fixed).
        sys.exit(0)

if __name__ == "__main__":
    main()
