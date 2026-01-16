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
    import sympy as sp
    try:
        with sp.evaluate(False):
            p = sp.S('Point2D(Integer(1),Integer(2))')
        # Normally, an error should not occur if the issue is fixed. So, if the code runs up to this point without exceptions,
        # it assumes the issue has been fixed. This expectation is based on the reported incorrect behavior.
        # However, if any AssertionError is caught here, it means the issue is not reproduced as the expectation is that
        # without the error the test should pass.
        print("The issue seems to be fixed.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        # Raises an AssertionError if an exception occurs, indicating the test failed to pass due to the intended issue.
        raise AssertionError("The issue is present.")

if __name__ == "__main__":
    test_issue()
