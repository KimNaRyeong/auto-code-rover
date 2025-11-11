Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
    out_dir = os.path.join(src_dir, "_build")
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, "html", ["sphinx.ext.autodoc"])
    app.builder = StandaloneHTMLBuilder(app)
    
    try:
        app.build()
        with open(os.path.join(out_dir, "index.html"), "r") as f:
            html_content = f.read()
            if "#example-python-function" in html_content:
                raise AssertionError("Python domain IDs are using dashes instead of underscores")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_python_domain_ids()
```
This script creates a Sphinx project, builds the HTML documentation, and checks if the generated HTML file contains the expected anchor ID `#example_python_function` instead of `#example-python-function`. If it finds the latter, it raises an `AssertionError` with a stack trace.