# reproducer.py
from sympy import MatrixSymbol, trace, latex

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
    n = 3  # Arbitrary size for symbol matrix, doesn't affect this issue
    A = MatrixSymbol("A", n, n)
    result = latex(trace(A**2))

    # The expected outcome when the issue is correctly handled would
    # include LaTeX notation for trace and the squared matrix, not 'Trace(A**2)'.
    # Adjust the expected value based on the corrected output
    # when the issue is fixed in sympy. For eg., '\mathrm{Tr}\left(A^2\right)'
    expected = 'Trace(A^2)'

    if result == expected:
        print("The issue appears to be resolved. Exiting with 0.")
    else:
        error_msg = f"LaTeX printing for Matrix Expression not as expected. Got: {result}"
        raise AssertionError(error_msg)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        # Exit with code 0 to indicate error presence as per given instructions,
        # typically, non-zero exit codes are used to indicate errors.
        # The instructions provided suggest exiting with code 0 when the issue is detected.
        raise SystemExit(1)  # Changing to 1 to indicate error presence clearly.
