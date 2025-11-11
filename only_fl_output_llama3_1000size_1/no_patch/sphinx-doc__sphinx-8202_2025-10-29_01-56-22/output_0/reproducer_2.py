import sys
from typing import Generic, TypeVar, ClassVar, Type
import traceback

_ValueType = TypeVar('_ValueType')

class MyGeneric(Generic[_ValueType]):
    #: Doc comment example.
    some_type: ClassVar[Type['MyGenericChild']]

class MyGenericChild(MyGeneric[_ValueType]):
    def __init__(self, inner_value: _ValueType) -> None:
        pass

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

def main():
    try:
        from docutils import nodes
        from sphinx.ext import autodoc

        class MyGenericChild(MyGeneric[_ValueType]):
            def __init__(self, inner_value: _ValueType) -> None:
                pass

        MyGeneric.some_type = MyGenericChild
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected warning")

if __name__ == "__main__":
    main()
