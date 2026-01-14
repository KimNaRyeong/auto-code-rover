 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import sphinx
from sphinx.ext.autodoc import ClassDocumenter

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class CustomClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        print("add_directive_header called with sig:", sig)
        super().add_directive_header(sig)

class CustomAutodoc(sphinx.ext.autodoc.Autodoc):
    def run(self):
        print("run called")
        return super().run()

def setup(app):
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-signature', CustomAutodoc().run)
    app.connect('autodoc-process-docstring', CustomClassDocumenter().add_directive_header)

if __name__ == "__main__":
    try:
        # Register the custom documenter
        from sphinx.ext.autodoc import setup as autodoc_setup
        autodoc_setup( CustomClassDocumenter(None, None, _autodoc_context = {}) )

        # Create a dummy class with a @classmethod @property
        class A:
            @classmethod
            @property
            def f(cls):
                """Some class property."""
                return "property"

        # Initialize the Sphinx application
        app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.', doctreedir='.', buildername='html', confoverrides={
            'autodoc_member_order': 'bysource',
            'autoclass_content': 'both',
        })

        # Set the custom documenter
        app.connect('autodoc-process-signature', CustomAutodoc().run)
        app.connect('autodoc-process-docstring', CustomClassDocumenter().add_directive_header)

        # Generate the documentation
        app.build(force_all=True)

        # Check if the documentation was generated correctly
        assert 'Some class property.' in open('_build/html/A.html').read()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
The script initializes a Sphinx application, creates a dummy class with a `@classmethod @property`, and generates the documentation. If the issue is present, the script will raise an `AssertionError` when checking if the documentation was generated correctly.

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is fixed, the script should exit with code 0. If the issue is present, the script will print a stack trace and exit with code 1.