Here is the `reproducer.py` file to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import Documenter
from docutils.parsers.rst import Directive

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

def test_python_domain_ids():
    app = Sphinx(srcdir='.', confdir='.')
    app.builder.init()
    
    documenter = Documenter(app, 'python')
    directive = Directive('py:function:: example_python_function(foo)\n\n    Some function.\n')
    node = documenter.generate(directive, 0)
    
    anchor = node[0]['ids'][0]
    assert anchor == 'example-python-function', f"Expected 'example-python-function' but got '{anchor}'"
    
    print("Issue is fixed!")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a Sphinx application, initializes the builder, and then uses the `Documenter` to generate a node from an RST directive that defines a Python function with underscores in its name. It then checks if the generated anchor ID contains dashes instead of underscores. If it does, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

You can run this script using `python3 reproducer.py`, and it should raise an `AssertionError` if the issue is present, or print "Issue is fixed!" if the issue is fixed.