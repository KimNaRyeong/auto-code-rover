Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import mock

# Create a sample generically-typed class
from typing import TypeVar, Generic
T = TypeVar('T')
class MyClass(Generic[T]):
    pass

# Create a mock object for autodoc
mock_obj = mock.Mock()
mock_obj.__module__ = 'my_module'
mock_obj.__name__ = 'MyClass'

try:
    # Attempt to make a subclass of the mock object, which should throw a TypeError
    mock._make_subclass(mock_obj, 'MySubClass')
except TypeError as e:
    print_stacktrace(e)
    raise AssertionError("TypeError raised when building docs for generically-typed class")
else:
    print("No error raised, issue is fixed!")
```
This script creates a sample generically-typed class `MyClass` and attempts to create a mock object for autodoc using the `mock` module. It then tries to make a subclass of the mock object using `mock._make_subclass`, which should throw a `TypeError` due to the issue with generic types.

If the issue is present, the script will raise an `AssertionError` and print the stack trace of the error. If the issue is fixed, the script will exit with code 0 and print "No error raised, issue is fixed!".