Here is the reproducer script:

```python
from typing import Generic, TypeVar
import sphinx
import sys
import traceback

_ValueType = TypeVar('_ValueType')

class MyGeneric(Generic[_ValueType]):
    #: Doc comment example.
    some_type: ClassVar[Type['MyGenericChild']]

class MyGenericChild(MyGeneric[_ValueType]):
    def __init__(self, inner_value: _ValueType) -> None:
        pass

try:
    from sphinx import conf
    from sphinx.util import logging
    from sphinx.ext import autodoc
    autodoc.process_doc(None)
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected no warning"
```

This script should be placed in a file named `reproducer.py` and executed by running `python3 reproducer.py`. If the issue is present, it will raise an AssertionError with the stack trace of the error.