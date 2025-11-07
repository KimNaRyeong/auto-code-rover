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

def test_idx_bounds_should_be_integers():
    import sympy as sp
    try:
        m, n = sp.symbols("m, n", real=True)
        # This should raise an error but does not; demonstrating the issue.
        i = sp.Idx("i", (m, n))
    except TypeError as e:
        print("Test passed: TypeError was raised as expected.")
        return
    except Exception as e:
        print("Unexpected error occurred.")
        print_stacktrace(e)
        raise e

    # If no error is raised, the test fails.
    raise AssertionError("Idx object accepted non-integer bounds without raising an error.")

if __name__ == "__main__":
    try:
        test_idx_bounds_should_be_integers()
    except AssertionError as e:
        print_stacktrace(e)
        raise e
