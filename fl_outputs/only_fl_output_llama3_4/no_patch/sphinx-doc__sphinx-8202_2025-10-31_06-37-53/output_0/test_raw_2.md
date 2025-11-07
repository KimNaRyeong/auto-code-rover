Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
from typing import Generic, TypeVar, ClassVar, Type

_ValueType = TypeVar('_ValueType')
class MyGeneric(Generic[_ValueType]):
    #: Doc comment example.
    some_type: ClassVar[Type['MyGenericChild']]

class MyGenericChild:
    pass

try:
    from sphinx.ext import autodoc
    autodoc.generate_doc(__name__)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    assert False, "Expected AssertionError"
    sys.exit(0)

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

This script attempts to generate Sphinx documentation for the `MyGeneric` class. If the issue is present, it will raise an `AssertionError` and print the stack trace.