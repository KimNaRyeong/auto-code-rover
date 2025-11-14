Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ModuleDocumenter
from docutils.core import publish_string

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

def test_documentation():
    app = Sphinx(srcdir=os.path.dirname(__file__), confdir=os.path.dirname(__file__))
    app.add_autodocumenter(ModuleDocumenter)
    
    try:
        doc = publish_string(app.builder.render('module', BaseClass.__module__), writer_name='html')
        assert 'Some class property' in doc
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    test_documentation()
```
This script defines a `BaseClass` with a method decorated with both `@classmethod` and `@property`. It then uses Sphinx to generate HTML documentation for this module. The script checks if the generated documentation contains the docstring of the method, and raises an `AssertionError` if it does not. If the issue is present, the script prints a stack trace of the error and exits with code 1. If the issue is fixed, the script exits with code 0.