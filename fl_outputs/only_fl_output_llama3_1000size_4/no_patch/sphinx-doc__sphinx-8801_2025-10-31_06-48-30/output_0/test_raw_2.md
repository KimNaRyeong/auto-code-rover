Here is the reproducer script:

```python
def main():
    try:
        import sphinx.ext.autodoc
        from sphinx.util.docstrings import prepare_docstring

        class Foo:
            """docstring"""
            attr1: int  #: docstring

        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        from sphinx.ext import autodoc

        def process_docstring(app, what, name, obj, options, lines):
            if isinstance(obj, type) and hasattr(obj, 'attr1'):
                raise AssertionError("Bar.attr1 is not documented")

        app = autodoc.AutoDocument()
        app.connect('autodoc-process-docstring', process_docstring)
        autodoc.process(Foo, Bar)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()

```

This script defines the same classes `Foo` and `Bar` as in your example. It then attempts to process these classes using Sphinx's autodoc module, which should raise an AssertionError if the issue is present.