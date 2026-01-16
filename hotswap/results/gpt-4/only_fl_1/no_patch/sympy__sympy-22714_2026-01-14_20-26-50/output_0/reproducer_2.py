# reproducer.py

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
            # Attempt to use Point2D with evaluate set to False, expected to fail if issue is present
            p = sp.S('Point2D(Integer(1), Integer(2))')
        # If the above code did not raise an exception, assume the issue is fixed
        print("The issue seems to be fixed, no exception was raised.")
        exit(0)  # Exit with code 0 indicating absence of the issue or successful workaround
    except ValueError as e:
        # If the specific expected exception is caught, print its stack trace to stderr
        print_stacktrace(e)
        # Raising an AssertionError indicates this test failed due to the existing issue
        raise AssertionError("The issue is reproduced, indicating it is still present.")

if __name__ == "__main__":
    test_issue()
