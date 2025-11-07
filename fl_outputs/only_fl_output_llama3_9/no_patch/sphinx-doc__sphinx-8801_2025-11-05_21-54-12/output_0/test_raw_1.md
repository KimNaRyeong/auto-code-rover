Here is a new reproducer script:

```python
import sphinx.ext.autodoc
from docutils import nodes

def main():
    try:
        class Foo:
            """docstring"""
            attr1: int  #: docstring

        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        from sphinx.ext import autodoc
        autodoc.autodoc(Bar, members=True, inherited_members=True)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script should be run with `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.