Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import Directive
from docutils.statemachine import ViewList

class ReproducerClass:
    @classmethod
    @property
    def reproducer_class_property(cls):
        """This is a class property."""
        return "reproducer"

def setup(app):
    app.add_autodocumenter(lambda obj: True)
    app.connect('autodoc-process-docstring', process_docstring)

def process_docstring(app, what, name, obj, options, lines):
    if what == 'class' and name == ReproducerClass.__name__:
        lines.extend(['.. autoclass:: %s' % name])

if __name__ == '__main__':
    try:
        src_dir = os.path.dirname(__file__)
        out_dir = os.path.join(src_dir, '_build')
        app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'html', ['sphinx.ext.autodoc'])
        app.setup_extension('reproducer')
        app.build()
        
        with open(os.path.join(out_dir, 'index.html'), 'r') as f:
            content = f.read()
            if 'This is a class property.' not in content:
                raise AssertionError("Class method decorated with @classmethod and @property was not documented.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script sets up a Sphinx project, defines a class with a class method decorated with both `@classmethod` and `@property`, and then builds the documentation. It checks if the docstring of the class property is present in the generated HTML file. If not, it raises an `AssertionError`.