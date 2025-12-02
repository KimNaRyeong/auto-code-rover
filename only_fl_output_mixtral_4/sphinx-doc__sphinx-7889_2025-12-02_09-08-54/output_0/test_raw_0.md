 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import typing
import unittest.mock as mock

from typing import TypeVar

T = TypeVar('T')

class GenericClass(object):
    def __init__(self, value: T):
        self.value = value

def mock_make_subclass(mocked_class, name, bases, namespace, **kwargs):
    mock_class = mock.mock_open().return_value.__enter__().__class__(name, bases, namespace)
    mock_class.__module__ = mocked_class.__module__
    return mock_class

mock._make_subclass = mock_make_subclass

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    try:
        # The following line will raise a TypeError when run with Sphinx's autodoc extension
        #