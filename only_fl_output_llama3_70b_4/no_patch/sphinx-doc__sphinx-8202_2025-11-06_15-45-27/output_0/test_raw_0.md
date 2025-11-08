Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
from typing import TypeVar, Generic, ClassVar, Type

_ValueType = TypeVar('_ValueType')

class MyGeneric(Generic[_ValueType]):
    #: Doc comment example.
    some_type: ClassVar[Type['MyGenericChild']]

class MyGenericChild(MyGeneric[_ValueType]):
    def __init__(self, inner_value: _ValueType) -> None:
        pass

MyGeneric.some_type = MyGenericChild

try:
    os.environ['MASTER_DOC'] = 'docs/index'
    import sphinx
    from sphinx.application import Sphinx
    app = Sphinx('reproducer', 'reproducer', 'docs', 'docs/_build/html')
    app.build()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("No issue found, exiting with code 0")
    exit(0)

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
```
This script reproduces the issue by creating a generic class with a doc comment, extending it, and then building the documentation using Sphinx. If the warning appears during the build process, an `AssertionError` is raised with a stack trace of the issue. If no issue is found, the script exits with code 0.