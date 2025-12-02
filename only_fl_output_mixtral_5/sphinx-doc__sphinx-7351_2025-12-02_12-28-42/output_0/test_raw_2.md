 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import sys
import sphinx
from docutils.core import publish_string
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutodocDirective

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup(app):
    app.add_directive('test', AutodocDirective)

def test_same_name_different_extensions():
    # Prepare the project directory
    project_dir = "test_project"
    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)

    # Create the necessary files
    with open("index.rst", "w") as index_file:
        index_file.write(".. toctree::\n   a.md\n")

    with open("a.md", "w") as md_file:
        md_file.write("# This is a.md\n")

    with open("a.rst", "w") as rst_file:
        rst_file.write("This is a.rst\n")

    # Initialize Sphinx
    srcdir = os.getcwd()
    confdir = os.path.join(srcdir, "_build")
    output_dir = os.path.join(srcdir, "_build", "html")
    app = Sphinx(srcdir, confdir, output_dir)
    app.setup_extension("myst_parser")
    app.connect('autodoc-process-docstring', lambda _app, what, name, obj, options, lines: lines)
    app.connect('builder-inited', setup)

    # Build the project
    try:
        app.build(app.config.tags)
    except Exception as e:
        print_stacktrace(e)
        assert False, "An exception should not be raised here"

    # Check the generated HTML
    with open(os.path.join(output_dir, "index.html")) as index_html:
        content = index_html.read()
        assert "This is a.rst" not in content, "a.rst should not be included in the generated HTML"
        assert "This is a.md" in content, "a.md should be included in the generated HTML"

if __name__ == "__main__":
    test_same_name_different_extensions()
    print("No issues found")
```
This script creates a Sphinx project with the necessary files to reproduce the issue, initializes Sphinx, builds the project, and checks the generated HTML. If the issue is present, an `AssertionError` will be raised, and if the issue is fixed, the script will print "No issues found".