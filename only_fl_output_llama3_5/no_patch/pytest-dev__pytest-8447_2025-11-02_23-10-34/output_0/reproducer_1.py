import pytest
from _pytest.nodes import File as PytestFile
from _pytest.nodes import Item as PytestItem

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

def pytest_collect_file(parent, path):
    return PytestFile.from_parent(parent, fspath=path)  # This line causes the error

if __name__ == "__main__":
    try:
        pytest_collect_file(None, "test_something.py")
    except TypeError as e:
        print_stacktrace(e)
        assert False, "Expected TypeError"
