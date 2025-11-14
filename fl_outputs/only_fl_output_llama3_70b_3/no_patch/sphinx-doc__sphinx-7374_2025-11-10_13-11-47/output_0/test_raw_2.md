Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
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
    src_dir = "_src"
    out_dir = "_build"

    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "index.rst"), "w") as f:
        f.write(".. py:function:: example_python_function\n")
    with open(os.path.join(src_dir, "conf.py"), "w") as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")

    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'html', False, [])
    app.add_domain(PythonDomain)
    try:
        app.build(force_all=True)
    except Exception as e:
        print_stacktrace(e)
        raise

    with open(os.path.join(out_dir, "index.html"), "r") as f:
        html_content = f.read()
        if "#example-python-function" in html_content:
            raise AssertionError("Python domain IDs are using dashes instead of underscores")

if __name__ == "__main__":
    test_python_domain_ids()
```
This script creates a Sphinx project, generates an RST file with a Python function, builds the HTML documentation, and checks if the generated HTML file contains the expected anchor ID `#example_python_function` instead of `#example-python-function`. If it finds the latter, it raises an `AssertionError` with a stack trace.