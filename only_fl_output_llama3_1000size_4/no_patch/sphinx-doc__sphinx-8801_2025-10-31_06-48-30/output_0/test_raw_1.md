Here is the reproducer script:

```python
import sphinx.ext.autodoc
from docutils import nodes
from sphinx.util.docstrings import prepare_docstring

def main():
    try:
        class Foo:
            """docstring"""
            attr1: int  #: docstring

        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        from sphinx.ext import autodoc
        from sphinx.util.docstrings import prepare_docstring

        def process_docstring(app, what, name, obj, options, lines):
            if isinstance(obj, type) and hasattr(obj, 'attr1'):
                raise AssertionError("Bar.attr1 is not documented")

        app = sphinx.Application()
        app.connect('autodoc-process-docstring', process_docstring)
        autodoc.process(Foo, Bar)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()

```

This script defines the same classes `Foo` and `Bar` as in your example. It then attempts to process these classes using Sphinx's autodoc module, which should raise an AssertionError if the issue is present.