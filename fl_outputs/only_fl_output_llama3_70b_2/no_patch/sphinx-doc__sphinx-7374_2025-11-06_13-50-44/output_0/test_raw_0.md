Here is the `reproducer.py` file to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder

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
    src_dir = 'docs'
    out_dir = '_build/html'

    # Create a sample reStructuredText document
    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write(".. py:function:: example_python_function(foo)\n\n")
        f.write("    Some function.\n")

    # Build the HTML documentation using Sphinx
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'html')
    app.builder = StandaloneHTMLBuilder(app)
    app.build()

    # Check if the anchor is generated with dashes instead of underscores
    with open(os.path.join(out_dir, 'index.html'), 'r') as f:
        html_content = f.read()
        if '#example-python-function' in html_content:
            raise AssertionError("Python domain IDs are using dashes instead of underscores")
        else:
            print("Issue is fixed!")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
```
This script creates a sample reStructuredText document with a Python function, builds the HTML documentation using Sphinx, and checks if the anchor is generated with dashes instead of underscores. If the issue is present, it raises an `AssertionError` and prints a stack trace of the issue.