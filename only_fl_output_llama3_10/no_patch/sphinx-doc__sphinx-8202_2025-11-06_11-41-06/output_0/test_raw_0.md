Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sys
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
    sys.exit(1)

print("Issue not reproduced")
```

This script attempts to reproduce the issue by assigning a new value to `MyGeneric.some_type`. If an error occurs, it prints the stack trace and exits with code 1.