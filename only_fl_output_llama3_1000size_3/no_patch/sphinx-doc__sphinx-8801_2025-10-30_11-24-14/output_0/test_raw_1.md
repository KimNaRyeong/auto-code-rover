Here is the reproducer script:

```python
import sys
from sphinx.ext import autodoc
from sphinx.util import inspect
from io import StringIO

def main():
    try:
        class Foo:
            """docstring"""
            attr1: int  #: docstring

        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        buffer = StringIO()
        autodoc.autodoc(Bar, out=buffer)
        output = buffer.getvalue().strip()
        if "Bar.attr1" not in output:
            raise AssertionError("Bar.attr1 is not documented")
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script will execute the autodoc function and check if Bar.attr1 is documented. If it's not, an `AssertionError` will be raised with a stack trace.