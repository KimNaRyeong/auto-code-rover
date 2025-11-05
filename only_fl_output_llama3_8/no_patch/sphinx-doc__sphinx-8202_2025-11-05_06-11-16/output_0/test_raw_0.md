Here is the reproducer script:

```python
import sphinx
from typing import Generic, TypeVar
from sphinx.ext import autodoc

_ValueType = TypeVar('_ValueType')

class MyGeneric(Generic[_ValueType]):
    #: Doc comment example.
    some_type: ClassVar[Type['MyGenericChild']]

class MyGenericChild(MyGeneric[_ValueType]):
    def __init__(self, inner_value: _ValueType) -> None:
        pass

try:
    MyGeneric.some_type = MyGenericChild
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected no warning"
```

This script should be placed in a file named `reproducer.py` and executed by running `python3 reproducer.py`. If the issue is present, it will raise an AssertionError with the stack trace of the error.