Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from docutils.parsers.rst import directives, Directive
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.domains.python import PythonDomain

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
    src_dir = os.path.dirname(__file__)
    out_dir = os.path.join(src_dir, '_build')
    
    rst_content = """
.. py:function:: example_python_function(foo)

    Some function.
"""
    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write(rst_content)
    
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'html')
    app.builder = StandaloneHTMLBuilder(app)
    app.emit('doctree-resolved', app, app.env)

    doctree = app.env.get_doctree('index')
    domain = PythonDomain()
    func_node = next(node for node in doctree.traverse() if isinstance(node, domain.objecttypes[0]))
    anchor_id = func_node['ids'][0]

    if '_' in anchor_id:
        raise AssertionError("Python domain IDs are broken")
    else:
        print("Issue is fixed")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
```
This script creates a minimal Sphinx project, builds it, and checks the generated anchor ID for a Python function. If the issue is present (i.e., the anchor ID contains an underscore), it raises an `AssertionError` with a stack trace. If the issue is fixed, it prints a success message and exits with code 0.

Please note that this script requires the `sphinx` and `docutils` packages to be installed.