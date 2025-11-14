Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ModuleDocumenter

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

class BaseClass:
    @classmethod
    @property
    def baseclass_class_property(cls):
        """Some class property."""
        return "property"

def test_documentation():
    try:
        os.mkdir('docs')
        os.mkdir('docs/source')
        with open('docs/conf.py', 'w') as f:
            f.write("extensions = ['sphinx.ext.autodoc']\n")
        with open('docs/source/index.rst', 'w') as f:
            f.write("Module\n======\n.. automodule:: reproducer\n  :members:\n")
        
        app = Sphinx(srcdir='docs/source', confdir='docs', outdir='docs/_build/html')
        app.build()
        
        with open('docs/_build/html/reproducer.html', 'r') as f:
            html = f.read()
            assert 'Some class property' in html
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    test_documentation()
```
This script creates a Sphinx documentation project, generates HTML documentation for the `BaseClass`, and checks if the generated documentation contains the docstring of the method. If the issue is present, the script raises an `AssertionError` with a stack trace of the error and exits with code 1. If the issue is fixed, the script exits with code 0.

Please note that this script assumes that Sphinx is installed and available in the Python environment where it's executed.