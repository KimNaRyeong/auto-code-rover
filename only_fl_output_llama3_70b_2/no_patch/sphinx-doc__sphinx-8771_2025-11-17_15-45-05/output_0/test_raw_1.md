Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
# reproducer.py

import os
import sys
from sphinx.ext.autodoc import AutodocDirective
from sphinx.application import Sphinx

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

DEFAULT_OPTION = 'default'

def do_something(msg, option=DEFAULT_OPTION):
    """Do something"""
    pass

try:
    # Create a temporary directory for the Sphinx build
    tmp_dir = "tmp_sphinx_build"
    os.makedirs(tmp_dir, exist_ok=True)

    # Create a Sphinx configuration file
    with open(os.path.join(tmp_dir, "conf.py"), "w") as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")
        f.write("autodoc_mock_imports = []\n")

    # Create a Sphinx index file
    with open(os.path.join(tmp_dir, "index.rst"), "w") as f:
        f.write(".. autodoc:: do_something\n")

    # Run Sphinx
    app = Sphinx(tmp_dir, tmp_dir, tmp_dir, tmp_dir)
    app.builder.build_all()

    # Check the generated HTML file
    with open(os.path.join(tmp_dir, "_build", "html", "index.html"), "r") as f:
        html_content = f.read()
        if 'do_something(msg, option="default")' in html_content:
            raise AssertionError("Sphinx did not keep the original signature")
        elif 'do_something(msg, option=DEFAULT_OPTION)' in html_content:
            print("Issue is fixed!")
            sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```
This script creates a temporary directory for the Sphinx build, defines a function `do_something` with a default argument value, runs Sphinx to generate documentation, and checks the generated HTML file for the expected signature. If the issue is present, it raises an `AssertionError`.