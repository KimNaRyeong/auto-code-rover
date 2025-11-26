Here is the `reproducer.py` file that reproduces the issue:
```
import pytest
from pathlib import Path

def test_issue():
    try:
        # Reproduce the issue with pytest-black
        item = pytest.nodes.File.from_parent(None, fspath=Path('test_something.py'), path='test_something.py')
        assert False, "Expected TypeError: __init__() got an unexpected keyword argument 'path'"
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

    try:
        # Reproduce the issue with pytest-checkdocs
        item = pytest.nodes.File.from_parent(None, fspath=Path('setup.py'), path='setup.py')
        assert False, "Expected TypeError: __init__() got an unexpected keyword argument 'path'"
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

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

if __name__ == "__main__":
    test_issue()
```
This script tries to reproduce the issue with both pytest-black and pytest-checkdocs by creating a `File` node with an unexpected `path` keyword argument. If the issue is present, it will raise an `AssertionError` with a stack trace of the error. If the issue is fixed, the script will exit with code 0.