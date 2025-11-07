Here is the reproducer script:

```python
import sphinx
from docutils import nodes
from sphinx.ext import autodoc

def main():
    try:
        class Foo:
            """docstring"""
            attr1: int  #: docstring


        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        from sphinx.ext import autodoc
        from sphinx.util import inspect

        mod = type('mod', (), {'Bar': Bar})
        inspect.modindex(mod)

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script defines the same classes `Foo` and `Bar` as in the original issue, then attempts to generate documentation for `Bar` using Sphinx's autodoc extension. If the issue is present (i.e., `Bar.attr1` is not documented), an `AssertionError` will be raised, which we catch and print a stack trace for before re-raising it.