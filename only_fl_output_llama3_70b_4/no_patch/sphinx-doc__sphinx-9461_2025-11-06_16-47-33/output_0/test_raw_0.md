Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ModuleDocumenter
from docutils.statemachine import StringList

class BaseClass:
    @classmethod
    @property
    def baseclass_class_property(cls):
        """Some class property."""
        return "property"

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

def main():
    app = Sphinx(srcdir=os.path.dirname(__file__), confdir=os.path.dirname(__file__))
    app.add_autodocumenter(ModuleDocumenter)
    
    try:
        app.build(force_all=True, filenames=['reproducer'])
        html_file = os.path.join(app.outdir, 'reproducer.html')
        with open(html_file, 'r') as f:
            content = f.read()
            assert "Some class property" in content
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script creates a Sphinx application, defines a class with a `@classmethod` and `@property` decorated method, builds the documentation, and checks if the docstring is present in the generated HTML file. If not, it raises an `AssertionError` and prints the stack trace using the provided function.