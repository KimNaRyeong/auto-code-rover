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

def verify_issue():
    import os
    import sys
    import runpy

    # Insert a known value that should not be removed.
    test_path = "something"
    sys.path.insert(0, test_path)

    # Save a copy of sys.path for comparison.
    original_sys_path = sys.path[:]

    try:
        runpy.run_module('pylint', run_name="__main__", alter_sys=True)
    except Exception as e:
        # We're not focusing on exceptions from pylint execution itself.
        pass

    # Verify that the issue has been reproduced.
    try:
        # Check if the first item has been removed erroneously.
        assert sys.path[0] == test_path, "The first item of sys.path was incorrectly removed."

        # We are also expecting that sys.path[0] should be "", ".", or os.getcwd()
        # if the issue has been fixed as expected.
        correct_start = ["", ".", os.getcwd()]
        assert sys.path[0] in correct_start, "sys.path[0] is not '', '.', or os.getcwd() after running pylint."

        print("The issue has been fixed, exiting with code 0.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    verify_issue()
