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


def check_version_string(min_version: str, current_version: str) -> bool:
    """Perform a string-based comparison of versions."""
    return current_version >= min_version


def main():
    min_required_version = "0.6"
    test_version = "0.10"

    try:
        assert check_version_string(min_required_version, test_version), "Version check failed"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Version check passed. The issue is fixed.")


if __name__ == "__main__":
    main()
