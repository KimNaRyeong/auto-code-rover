Here is a new standalone Python script `reproducer.py` to reproduce the issue:
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
    src_dir = 'src'
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write("""
.. py:function:: example_python_function(foo)

    Some function.
""")
    app = Sphinx(src_dir, src_dir, 'build', 'build', 'html')
    app.builder = StandaloneHTMLBuilder(app)
    app.build()
    with open(os.path.join('build', 'index.html'), 'r') as f:
        html = f.read()
    if '#example-python-function' in html:
        raise AssertionError("Python domain IDs are using dashes instead of underscores")
    elif '#example_python_function' not in html:
        print("The issue is fixed!")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
```
This script uses the `sphinx` library to generate HTML documentation from a simple reStructuredText document containing a Python function with an underscore in its name. It then checks if the generated HTML file contains the expected anchor ID. If it doesn't, it raises an `AssertionError` with a stack trace.

Please note that this script requires the `sphinx` library to be installed. You can install it using `pip install sphinx`.