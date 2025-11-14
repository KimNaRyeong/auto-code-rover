from typing import TypeVar, Generic, ClassVar, Type
import subprocess
import os

_ValueType = TypeVar('_ValueType')

class MyGeneric(Generic[_ValueType]):
    #: Doc comment example.
    some_type: ClassVar[Type['MyGenericChild']]

class MyGenericChild(MyGeneric[_ValueType]):
    def __init__(self, inner_value: _ValueType) -> None:
        pass

MyGeneric.some_type = MyGenericChild

def generate_docs():
    try:
        import sphinx
        from sphinx.application import Sphinx
        app = Sphinx(srcdir=os.getcwd(), confdir=os.getcwd(), outdir='_build')
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
    else:
        print("No issue found")

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

generate_docs()
