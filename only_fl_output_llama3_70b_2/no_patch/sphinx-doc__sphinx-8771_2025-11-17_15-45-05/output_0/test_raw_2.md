Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
# reproducer.py

import os
import sys
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutodocDirective
from docutils.core import publish_string
from sphinx.ext.autosummary import Autosummary

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
    # Create a Sphinx configuration file
    conf_py = """
extensions = ['sphinx.ext.autodoc']
autodoc_mock_imports = []
"""

    # Create a Sphinx index file
    index_rst = """
.. autodoc:: do_something
"""

    # Run Sphinx
    app = Sphinx(srcdir="", outdir="", confdir="")
    app.builder.build_all()

    # Check the generated HTML file
    html_content = publish_string(index_rst, writer_name="html")
    if 'do_something(msg, option="default")' in html_content:
        raise AssertionError("Sphinx did not keep the original signature")
    elif 'do_something(msg, option=DEFAULT_OPTION)' in html_content:
        print("Issue is fixed!")
        sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```
This script creates a Sphinx configuration file and an index file, runs Sphinx to generate documentation, and checks the generated HTML content for the expected signature. If the issue is present, it raises an `AssertionError`.