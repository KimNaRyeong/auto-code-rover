import pytest
from _pytest.nodes import File as PytestFile
from _pytest.nodes import Item as PytestItem
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

def pytest_collect_file(parent, path):
    return PytestItem.from_parent(parent=parent, fspath=path, path=path)

def test_reproducer():
    try:
        pytest.main([path])
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError: __init__() got an unexpected keyword argument 'path'"

if __name__ == "__main__":
    test_reproducer()
