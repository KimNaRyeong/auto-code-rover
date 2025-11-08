import pytest
from _pytest.nodes import Node

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

def test_reproduce_issue():
    class BlackItem(Node):
        def __init__(self, parent, fspath, path, **kw):
            super().__init__(parent, fspath=fspath, path=path, **kw)

    try:
        BlackItem.from_parent(None, fspath='path', path='path')
    except TypeError as e:
        print_stacktrace(e)
        assert False, "TypeError: __init__() got an unexpected keyword argument 'path'"

if __name__ == '__main__':
    test_reproduce_issue()
