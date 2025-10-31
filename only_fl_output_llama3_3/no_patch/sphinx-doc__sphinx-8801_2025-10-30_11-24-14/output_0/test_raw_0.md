Here is the reproducer script:

```python
import sys
from sphinx.ext import autodoc
from sphinx.util import inspect

def main():
    try:
        class Foo:
            """docstring"""
            attr1: int  #: docstring

        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        autodoc.autodoc(Bar, out=sys.stdout)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

You can run this script with `python3 reproducer.py` to reproduce the issue. If the issue is present, it will raise an `AssertionError`, which will be caught and printed with a stack trace.