 Here is a revised standalone python file `reproducer.py` to reproduce the issue:
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
    app.add_autodocumenter(CustomClassDocumenter)
    app.connect('autodoc-process-docstring', CustomAutodoc().process_docstring)
    app.connect('autodoc-process-signature', CustomAutodoc().process_signature)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

if __name__ == '__main__':
    with open('dummy_module.py', 'w') as f:
        f.write('''
class MetaClass:
    @classmethod
    @property
    def metaclass_class_property(cls):
        """Metaclass class property docstring."""
        return "property"

    @classmethod
    @property
    def metaclass_abstract_class_property(cls):
        """Metaclass abstract class property docstring."""
        return "abstract property"

class BaseClass:
    @classmethod
    @property
    def baseclass_class_property(cls):
        """Base class class property docstring."""
        return "property"

    @classmethod
    @property
    def baseclass_abstract_class_property(cls):
        """Base class abstract class property docstring."""
        return "abstract property"

class SubClass(BaseClass):
    @classmethod
    @property
    def subclass_class_property(cls):
        """Sub class class property docstring."""
        return "property"

    @classmethod
    @property
    def subclass_abstract_class_property(cls):
        """Sub class abstract class property docstring."""
        return "abstract property"
        ''')

    app = sphinx.application.Sphinx(srcdir='.', builddir='.', config='.cfg')
    app.setup_extension('sphinx.ext.autodoc')
    app.setup_extension('sphinx.ext.autosummary')
    app.connect('autodoc-process-docstring', CustomAutodoc().process_docstring)
    app.connect('autodoc-process-signature', CustomAutodoc().process_signature)
    app.connect('builder-inited', CustomClassDocumenter().populate_directives)
    app.connect('autodoc-skip-member', CustomClassDocumenter().skip_member)
    app.connect('autodoc-process-signature', CustomClassDocumenter().handle_signature)
    app.connect('autodoc-process-docstring', CustomClassDocumenter().handle_docstring)
    app.connect('autodoc-default-flags', CustomClassDocumenter().default_flags)
    app.connect('autodoc-process-docstring', CustomClassDocumenter().add_directive_header)

    try:
        app.build(force_all=True, warningiserror=True)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
This revised version of