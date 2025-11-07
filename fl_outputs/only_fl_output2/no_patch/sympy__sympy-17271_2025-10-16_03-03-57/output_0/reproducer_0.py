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

def test_frac_zoo_issue():
    from sympy import frac, zoo

    # Wrapped with try-expect to capture and display the stack trace
    try:
        result = frac(zoo)
        # If no exception occurs, assert that the result is not a TypeError.
        # This might need to be adjusted based on the expected correct behavior.
        # For now, we expect any result that doesn't raise an exception.
        assert result is not None, "Expected a value, got None"
    except Exception as e:
        print_stacktrace(e)
        # Raising AssertionError to indicate the presence of the bug.
        raise AssertionError("Test failed due to unexpected issue.") from e

if __name__ == "__main__":
    test_frac_zoo_issue()
