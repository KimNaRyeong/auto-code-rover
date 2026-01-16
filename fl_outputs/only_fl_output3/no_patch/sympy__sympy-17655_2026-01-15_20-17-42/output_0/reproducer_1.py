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

def reproduce_issue():
    import sympy
    from sympy import geometry as ge
    import sys  # Ensure sys is imported for print_stacktrace functionality

    point1 = ge.Point(0, 0)
    point2 = ge.Point(1, 1)

    # This line works as expected
    try:
        result1 = point1 + point2 * sympy.sympify(2.0)
    except Exception as e:
        print("Unexpected exception on valid operation:")
        print_stacktrace(e)
        raise AssertionError("First operation caused an unexpected exception.")

    # This line should work similarly but raises an exception currently
    try:
        result2 = point1 + sympy.sympify(2.0) * point2
        assert result1 == result2, "Results should be the same"
        print("Issue has been resolved. Exiting with code 0.")
        exit(0)
    except Exception as e:
        # If an exception is raised, it's the current issue
        print("An exception occurred reproducing the issue:", file=sys.stderr)
        print_stacktrace(e)
        raise AssertionError("Expected both operations to be valid.") from e

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as ae:
        print(f"AssertionError: {ae}", file=sys.stderr)
        exit(1)  # Exit with a non-zero code to indicate failure/error
