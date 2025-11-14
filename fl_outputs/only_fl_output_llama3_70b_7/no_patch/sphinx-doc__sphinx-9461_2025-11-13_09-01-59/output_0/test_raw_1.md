Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.cmd.build import build_main
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
        with open('docs/conf.py', 'w') as f:
            f.write("extensions = ['sphinx.ext.autodoc']\n")
        with open('reproducer.py', 'r') as f:
            with open('docs/reproducer.py', 'w') as g:
                g.write(f.read())
        build_main(['-b', 'html', '.', '_build/html'])
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

    try:
        with open('_build/html/reproducer.html', 'r') as f:
            html = f.read()
            assert 'baseclass_class_property' in html
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    test_documentation()
```
This script creates a Sphinx documentation project, generates HTML documentation for the `reproducer.py` module, and checks if the method decorated with both `@classmethod` and `@property` is documented in the generated HTML file. If the method is not documented, it raises an `AssertionError` with a stack trace of the issue.