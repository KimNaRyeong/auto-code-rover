Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.builders.latex import LaTeXBuilder

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

def reproduce_issue():
    # Create a temporary directory for the project
    tmp_dir = "tmp_reproduce_issue"
    os.makedirs(tmp_dir, exist_ok=True)

    # Write the RST file
    with open(os.path.join(tmp_dir, "index.rst"), "w") as f:
        f.write("""
Test
====

Explicitly numbered footnotes
---------------------------

First reference to first footnote [1]_

First reference to second footnote [2]

Second reference to first footnote [1]

Second reference to second footnote [2]_


.. rubric:: Footnotes

.. [1] A first footnote

.. [2] A second footnote
""")

    # Configure Sphinx
    conf_py = os.path.join(tmp_dir, "conf.py")
    with open(conf_py, "w") as f:
        f.write("extensions = []\n")

    # Build the LaTeX PDF
    app = Sphinx(tmp_dir, tmp_dir, conf_py, os.path.join(tmp_dir, "_build"), "latex", verbosity=0)
    app.builder = LaTeXBuilder(app)

    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

    # Check the PDF output
    pdf_file = os.path.join(tmp_dir, "_build", "latex", "index.pdf")
    with open(pdf_file, "rb") as f:
        pdf_content = f.read().decode("latin-1")

    if "?" in pdf_content:
        raise AssertionError("Issue is present: ? character found in PDF output")

if __name__ == "__main__":
    reproduce_issue()
```
This script creates a temporary directory for the project, writes the RST file and `conf.py` file, builds the LaTeX PDF using Sphinx, and checks the PDF output for the presence of the `?` character. If the issue is present, it raises an `AssertionError` with a stack trace.