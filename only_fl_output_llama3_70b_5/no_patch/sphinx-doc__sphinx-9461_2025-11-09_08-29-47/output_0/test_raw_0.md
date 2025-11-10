Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import Directive

def test_documentation():
    class BaseClass:
        @classmethod
        @property
        def baseclass_class_property(cls):
            """Some class property."""
            return "property"

    src_dir = 'docs'
    out_dir = '_build/html'

    app = Sphinx(src_dir, src_dir, out_dir, 'dummy_module')
    app.add_directive('autoclass', Directive)
    app.build()

    with open(os.path.join(out_dir, 'dummy_module.html'), 'r') as f:
        html_content = f.read()

    if "baseclass_class_property" not in html_content:
        raise AssertionError("Method decorated with @classmethod and @property is not documented")

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

try:
    test_documentation()
except AssertionError as e:
    print_stacktrace(e)
```
This script creates a Sphinx project, defines a class with a method decorated with both `@classmethod` and `@property`, builds the documentation, and checks if the method is documented in the generated HTML. If not, it raises an `AssertionError`.