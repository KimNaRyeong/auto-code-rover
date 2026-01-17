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

def test_issue():
    from sympy import I, MatrixSymbol

    M = MatrixSymbol('M', 2, 2)
    try:
        # The line that is expected to raise an exception due to the issue
        print(I*M)
        # If the previous line does not raise an exception, it means the issue is fixed
        print('Issue seems to be fixed. Exiting with code 0.')
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        # Raising an AssertionError to indicate the presence of the reported issue
        raise AssertionError("The issue is still present.")

if __name__ == "__main__":
    test_issue()
