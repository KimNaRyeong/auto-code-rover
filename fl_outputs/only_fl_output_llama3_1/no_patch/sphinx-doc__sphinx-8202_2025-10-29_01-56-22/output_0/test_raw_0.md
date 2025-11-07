Here is the reproducer script:

```python
import sys
from typing import Generic, TypeVar, ClassVar, Type
from sphinx.application import SphinxApplication

_ValueType = TypeVar('_ValueType')

class MyGeneric(Generic[_ValueType]):
    #: Doc comment example.
    some_type: ClassVar[Type['MyGenericChild']]

class MyGenericChild(MyGeneric[_ValueType]):
    def __init__(self, inner_value: _ValueType) -> None:
        pass

def main():
    try:
        MyGeneric.some_type = MyGenericChild
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected no warning")

if __name__ == "__main__":
    main()
```

This script will attempt to reassign the `some_type` attribute of the `MyGeneric` class with a new value. If an error occurs, it will catch the exception and print the stack trace using the provided function.