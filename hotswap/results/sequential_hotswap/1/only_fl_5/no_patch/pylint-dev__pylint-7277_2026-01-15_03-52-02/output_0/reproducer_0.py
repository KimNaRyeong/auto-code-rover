# reproducer.py
def main():
    import os
    import sys
    import runpy

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

    # Add a recognizable item in sys.path's first position
    test_path = "unique_path_to_test_presence"
    sys.path.insert(0, test_path)

    # Attempt to run pylint through runpy, mimicking the issue scenario.
    try:
        runpy.run_module('pylint', run_name="__main__", alter_sys=True)
    except Exception as e:
        print_stacktrace(e)

    # Check if the first item of sys.path was modified unexpectedly
    assert sys.path[0] == test_path, "The first item of sys.path was unexpectedly modified."

    # If the script gets here without raising an AssertionError, print success message.
    print("Success: The issue is not present.")

if __name__ == "__main__":
    main()
