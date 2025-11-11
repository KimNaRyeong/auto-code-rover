Here is the `reproducer.py` script to reproduce the issue:
```
import os
import shutil
from sphinx.application import Sphinx
from myst_parser import Parser

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
    project_dir = "temp_project"
    os.makedirs(project_dir, exist_ok=True)

    # Create files with same name but different extensions
    index_rst_path = os.path.join(project_dir, "index.rst")
    a_md_path = os.path.join(project_dir, "a.md")
    a_rst_path = os.path.join(project_dir, "a.rst")

    with open(index_rst_path, "w") as f:
        f.write(".. toctree::\n    a.md\n")

    with open(a_md_path, "w") as f:
        f.write("This is a Markdown file.\n")

    with open(a_rst_path, "w") as f:
        f.write("This is a reStructuredText file.\n")

    # Configure Sphinx
    conf_py_path = os.path.join(project_dir, "conf.py")
    with open(conf_py_path, "w") as f:
        f.write("extensions = ['myst_parser']\n")

    # Build the documentation
    app = Sphinx(project_dir, project_dir, conf_py_path, project_dir)
    app.builder.init()

    try:
        app.build()
        # Check if the correct file is included in the document
        with open(os.path.join(project_dir, "_build", "index.html"), "r") as f:
            html_content = f.read()
            assert "This is a Markdown file" in html_content, "Expected 'a.md' to be included in the document"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```
This script creates a temporary project directory with the necessary files (`index.rst`, `a.md`, and `a.rst`) and configures Sphinx to use the `myst_parser` extension. It then builds the documentation and checks if the correct file (`a.md`) is included in the generated HTML document. If not, it raises an `AssertionError` with a stack trace of the issue.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.