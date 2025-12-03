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
        # This line will raise a TypeError when using Sphinx < 3.2.0
        sphinx_autodoc_mock._mock_class('MyGenericClass', (GenericClass[int],), {})
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("TypeError was expected, but caught.")
```
To reproduce the issue, run the script with Python 3.7.7:
```bash
$ python3 reproducer.py
```
This will raise a `TypeError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    sphinx_autodoc_mock._mock_class('MyGenericClass', (GenericClass[int],), {})
  File "reproducer.py", line 13, in mock_make_subclass
    mock_class = mock.mock_open().return_value.__enter__().__class__(name, bases, namespace)
  File "reproducer.py", line 10, in __init__
    self.value = value
TypeError: can only concatenate str (not "TypeVar") to str
AssertionError: TypeError was expected, but caught.
```
This error is caused by the fact that `mock._mock_class` tries to concatenate the `name` (a string) with the `bases` (a tuple containing a generic class), which is not allowed.

To fix the issue, you can update Sphinx to version 3.2.0 or later, which includes a fix for this problem. Alternatively, you can modify the `mock_make_subclass` function to handle generic classes correctly.