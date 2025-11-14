Here is the `reproducer.py` file to reproduce the issue:
```
import os
import pytest
from _pytest.config import Config

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

def test_log_file_issue():
    config = Config()
    try:
        pytest.main(['--log-file=subtest/test.log'], config)
    except FileNotFoundError as e:
        print_stacktrace(e)
        assert False, "Expected --log-file to create subdirectories"

if __name__ == "__main__":
    test_log_file_issue()
```
This script will execute `pytest` with the `--log-file` option set to a path that includes a non-existent subdirectory. If the issue is present, it should raise an `AssertionError` and print the stack trace of the `FileNotFoundError`. If the issue is fixed, the script will exit with code 0.