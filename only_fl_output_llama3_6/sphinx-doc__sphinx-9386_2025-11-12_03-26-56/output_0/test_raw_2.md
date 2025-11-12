Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc
from docutils import nodes
from docutils.statemachine import StringList

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

def reproduce_issue():
    try:
        from sphinx.application import SphinxApplication
        app = SphinxApplication()
        app.builder = autodoc.AutoDocumentBuilder(app, outdir='.')

        class TestClass:
            @property
            def test_property(self) -> int:
                return 0

        config = app.config
        config.autodoc_typehints = 'none'
        from sphinx.ext import autodoc
        autodoc.generate_doc([TestClass], output_path='docs', title='Test Class')

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script defines a simple class with a property and attempts to generate documentation for it using Sphinx's `autodoc` extension. The `reproduce_issue` function sets the `autodoc_typehints` configuration option to `'none'`, which should prevent type hints from being rendered in the output. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed.