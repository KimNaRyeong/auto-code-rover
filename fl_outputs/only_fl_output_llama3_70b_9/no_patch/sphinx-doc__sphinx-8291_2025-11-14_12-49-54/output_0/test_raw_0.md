Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutoDirective
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList

class MyException:
    """My Exception class.

    Attributes:
        message (str): The exception message.
    """
    message: str

def setup(app):
    app.add_directive('automodule', AutoDirective)
    app.connect('autodoc-process-docstring', process_docstring)

def process_docstring(app, what, name, obj, options, lines):
    return lines

if __name__ == '__main__':
    try:
        # Create a temporary directory for the documentation
        doc_dir = 'doc_test'
        os.makedirs(doc_dir, exist_ok=True)
        
        # Create a conf.py file
        with open(os.path.join(doc_dir, 'conf.py'), 'w') as f:
            f.write("extensions = ['sphinx.ext.autodoc']\n")
            f.write("napoleon_use_ivar = True\n")
        
        # Create an index.rst file
        with open(os.path.join(doc_dir, 'index.rst'), 'w') as f:
            f.write(".. automodule:: my_module\n")
            f.write("   :members:\n")
            f.write("   :undoc-members:\n")
        
        # Build the documentation
        app = Sphinx(srcdir=doc_dir, confdir=doc_dir, outdir=os.path.join(doc_dir, '_build'))
        app.build()
        
        # Check if the attribute is duplicated in the generated documentation
        with open(os.path.join(doc_dir, '_build', 'html', 'my_module.html'), 'r') as f:
            html_content = f.read()
            assert '<dt>message</dt>' not in html_content or '<dt>str</dt>' not in html_content, "Attribute is duplicated in the generated documentation"
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)
```
This script creates a temporary directory for the documentation, generates an `index.rst` file with an `automodule` directive, and builds the documentation using Sphinx. It then checks if the attribute is duplicated in the generated HTML file. If it is, the script raises an `AssertionError`.