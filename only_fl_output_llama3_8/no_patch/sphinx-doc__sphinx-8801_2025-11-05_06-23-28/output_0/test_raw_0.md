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

        mod = object()
        mod.Bar = Bar

        def process_docstring(node, name):
            return node.children[0].text

        autodoc.process_docstring = process_docstring

        # This should raise an AssertionError if the issue is present
        inspect.autodoc(Bar)

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script defines two classes `Foo` and `Bar`, then attempts to generate documentation for `Bar` using Sphinx's autodoc extension. If the issue is present, an `AssertionError` should be raised, which will be caught by the script and printed with a stack trace.