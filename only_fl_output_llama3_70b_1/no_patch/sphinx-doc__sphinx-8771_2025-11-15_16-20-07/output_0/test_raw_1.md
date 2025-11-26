Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
# reproducer.py

import os
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

# Create a temporary directory for the Sphinx build
tmp_dir = "tmp"
os.makedirs(tmp_dir, exist_ok=True)

# Create a Sphinx configuration file
with open(os.path.join(tmp_dir, "conf.py"), "w") as f:
    f.write("extensions = ['sphinx.ext.autodoc']\n")

# Create a Sphinx project
project = "myproject"
author = "Me"

app = Sphinx(tmp_dir, tmp_dir, os.path.join(tmp_dir, "_build"), os.path.join(tmp_dir, "_build", "html"),
             project, author, [AutodocDirective])

try:
    # Add the module to the Sphinx project
    app.add_module("mymodule", "mymodule.py")

    # Write the module file
    with open(os.path.join(tmp_dir, "mymodule.py"), "w") as f:
        f.write("DEFAULT_OPTION = 'default'\n")
        f.write("def do_something(msg, option=DEFAULT_OPTION):\n")
        f.write("    pass\n")

    # Build the Sphinx project
    app.build()

    # Check if the generated documentation has the correct signature
    with open(os.path.join(tmp_dir, "_build", "html", "mymodule.html"), "r") as f:
        html = f.read()
        assert "do_something(msg, option=DEFAULT_OPTION)" in html, "Incorrect signature"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script creates a temporary Sphinx project, adds a module with the `do_something` function, builds the documentation, and checks if the generated HTML file has the correct signature. If the signature is incorrect, it raises an `AssertionError` with a stack trace.

Please note that you need to have Sphinx installed in your environment for this script to work.