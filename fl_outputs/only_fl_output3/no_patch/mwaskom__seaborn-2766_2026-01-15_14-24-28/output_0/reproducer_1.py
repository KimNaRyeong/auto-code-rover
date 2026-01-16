import subprocess
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_seaborn_warning():
    try:
        import seaborn  # noqa: F401
        assert False, "Expected a DeprecationWarning but none was raised."
    except DeprecationWarning as warning:
        if "distutils Version classes are deprecated. Use packaging.version instead." in str(warning):
            print("DeprecationWarning for distutils version classes detected.")
        else:
            assert False, "Different DeprecationWarning detected."
    except AssertionError as e:
        raise
    except Exception as e:
        assert False, f"Unexpected error occurred: {e}"

if __name__ == "__main__":
    try:
        check_seaborn_warning()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate the issue is present

    print("No issue detected.")
    sys.exit(0)  # Exit with code 0 to indicate the issue is fixed or not present
