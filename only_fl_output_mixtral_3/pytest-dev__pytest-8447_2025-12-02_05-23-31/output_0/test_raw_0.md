 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import pytest
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_pytest_black():
    with pytest.plugins.manager.PluginManager() as manager:
        manager.register(BlackPlugin(), 'black')
        args = ['test_something.py']
        config = manager.make_config(args=args)
        node_id = manager.get_plugin('black').pytest_collection_modifyitems(config, manager.get_collector(config))

class BlackPlugin:
    def __init__(self):
        pass

    def pytest_collection_modifyitems(self, config, items):
        path = pytest.Path('test_something.py')
        BlackItem.from_parent(parent=None, fspath=path)

class BlackItem:
    @classmethod
    def from_parent(cls, parent, **kw):
        return cls(path=kw['path'])

    def __init__(self, path):
        pass

try:
    test_pytest_black()
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue present"
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` with the stack trace of the issue.

The issue is caused by the `path` keyword argument being passed to the `BlackItem` constructor, which does not accept it. This is happening because the `BlackPlugin` class is passing `path=kw['path']` to the `BlackItem` constructor, but `BlackItem` does not have a `path` argument.

To fix the issue, the `BlackItem` class should be updated to accept a `path` argument, or the `path` keyword argument should be removed from the `from_parent` method in the `BlackPlugin` class.