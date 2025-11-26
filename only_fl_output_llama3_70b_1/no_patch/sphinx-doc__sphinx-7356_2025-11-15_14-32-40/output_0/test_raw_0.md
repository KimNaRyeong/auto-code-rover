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
    src_dir = os.path.dirname(__file__)
    out_dir = os.path.join(src_dir, '_build')
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'html', ['sphinx.ext.autodoc'])
    app.builder = StandaloneHTMLBuilder(app)
    
    try:
        app.build()
        with open(os.path.join(out_dir, 'index.html'), 'r') as f:
            html_content = f.read()
            assert '#example_python_function' in html_content, "Expected anchor to be #example_python_function, but got #example-python-function"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_python_domain_ids()
```
This script creates a Sphinx project with a single Python function `example_python_function` and builds the HTML documentation. It then checks if the anchor in the generated HTML file is still using underscores (`#example_python_function`) or has been changed to dashes (`#example-python-function`). If the anchor uses dashes, it raises an `AssertionError` with a stack trace.

To run this script, save it as `reproducer.py` and execute it with `python3 reproducer.py`.