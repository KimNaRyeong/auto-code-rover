import importlib.util
import sys
from unittest.mock import patch

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

def main():
    import sys
    if len(sys.argv) != 2 or sys.argv[1] != "foo.bar.baz":
        raise AssertionError("Expected -m foo.bar.baz as the command-line argument")

if __name__ == "__main__":
    with patch("sys.argv", ["python", "-m", "foo.bar.baz"]):
        try:
            main()
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)
        else:
            sys.exit(0)
