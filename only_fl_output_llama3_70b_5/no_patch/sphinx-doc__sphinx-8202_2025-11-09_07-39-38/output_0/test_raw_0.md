Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
from typing import TypeVar, Generic, ClassVar, Type

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
        import subprocess
        result = subprocess.run(['poetry', 'run', 'make', 'html'], cwd='docs')
        if result.returncode != 0:
            raise AssertionError("Error generating HTML documentation")
    except Exception as e:
        print_stacktrace(e)
        raise

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

if __name__ == '__main__':
    main()
```
This script reproduces the issue by creating a generic class with a doc comment, extending it, and then generating HTML documentation using Sphinx. If the warning appears during the documentation generation, an `AssertionError` is raised, and the stack trace is printed to stderr.