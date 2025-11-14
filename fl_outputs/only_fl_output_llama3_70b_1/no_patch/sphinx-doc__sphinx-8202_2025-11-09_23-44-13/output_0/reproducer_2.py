from typing import TypeVar, Generic, ClassVar, Type
import os
import sys

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
        from sphinx.ext.autodoc import Directive
        from docutils.parsers.rst import directives
        directive = Directive('automodule', ['lib.test'], 1, 1, 1)
        directives.register_directive('automodule', directive)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue is present"
    else:
        print("Issue is fixed, no warning was raised.")
        return 0

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

if __name__ == "__main__":
    exit(main())
