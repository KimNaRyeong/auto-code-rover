Here is a new standalone Python file `reproducer.py` to reproduce the issue:
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
    try:
        src_dir = 'src'
        os.makedirs(src_dir, exist_ok=True)
        with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
            f.write("""
.. py:function:: example_python_function(foo)

    Some function.
""")
        app = Sphinx(src_dir, src_dir, 'build', 'build', 'html')
        app.builder = StandaloneHTMLBuilder(app)
        app.build(force_all=True)
        with open(os.path.join('build', 'index.html'), 'r') as f:
            html_content = f.read()
            expected_anchor = 'example-python-function'
            actual_anchor = [line for line in html_content.splitlines() if 'href' in line][0].split('"')[1]
            assert actual_anchor == expected_anchor
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_python_domain_ids()
```
This script uses the `sphinx` library to generate HTML from a reStructuredText file, and checks if the generated anchor for a Python function with an underscore in its name uses dashes instead of underscores. If the issue is present, it raises an `AssertionError` with a stack trace.

Please note that this script requires the `sphinx` library to be installed. You can install it using `pip install sphinx`.