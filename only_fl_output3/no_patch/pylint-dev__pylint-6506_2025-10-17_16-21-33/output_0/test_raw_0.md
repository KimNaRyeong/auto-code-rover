Below is a `reproducer.py` script designed to run in the root directory of the pylint project. This script will attempt to execute `pylint` with an unrecognized option (`-Q`) programmatically and check if the behavior matches the expected: outputting a simple error message without a full traceback. It utilizes subprocess to run the pylint command and captures its output and error messages.

```python
import subprocess
import sys

def reproduce_issue():
    try:
        # Assuming pylint is installed in the environment and available as a command
        result = subprocess.run(['pylint', '-Q'], capture_output=True, text=True, check=True)
        print("Output:", result.stdout)
        print("Error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        # We check if the error message is as expected without a full traceback
        assert "Traceback" not in e.stderr, "Traceback should not be present in the error for unrecognized options"
        # Additional assert to check for expected hint for usage or error message could be added here
        raise AssertionError("Issue reproduced: Unrecognized option results in an unexpected traceback.") from e

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

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    print("No issue detected. Pylint behaves as expected.")
    sys.exit(0)
```

This script runs `pylint` with an unrecognized option and listens for an error that includes a traceback. The custom `print_stacktrace` function formats and prints the traceback if it's part of the error output. The script asserts that a traceback should not be present when passing an unrecognized option to `pylint` and raises an `AssertionError` if the issue is reproduced, indicating that the problem still exists. If no issue is found (i.e., pylint correctly handles unrecognized options without printing a traceback), the script exits with a code 0, indicating success.