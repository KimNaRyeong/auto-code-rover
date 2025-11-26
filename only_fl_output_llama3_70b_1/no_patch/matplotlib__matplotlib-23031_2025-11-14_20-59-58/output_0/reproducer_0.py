import matplotlib as mpl
from unittest import mock
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    with mock.patch("locale.getpreferredencoding", return_value="utf-32-be"):
        try:
            import matplotlib
            assert False, "Expected UnicodeDecodeError"
        except UnicodeDecodeError as e:
            print_stacktrace(e)
            sys.exit(1)  # Exit with code 1 if the issue is present

if __name__ == "__main__":
    main()
