Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
import shutil
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
        f.write("This is a markdown file.\n")

    with open(a_rst_path, "w") as f:
        f.write("This is a reStructuredText file.\n")

    # Configure Sphinx
    conf_py_path = os.path.join(project_dir, "conf.py")
    with open(conf_py_path, "w") as f:
        f.write("extensions = ['myst_parser']\n")

    # Build the documentation
    app = Sphinx(project_dir, project_dir, project_dir, project_dir)
    app.build()

    # Check if the issue is present
    built_html_path = os.path.join(project_dir, "_build", "html", "index.html")
    with open(built_html_path, "r") as f:
        html_content = f.read()
        assert "This is a markdown file." in html_content, "Expected to find markdown content"
        print("Issue not present. Exiting with code 0.")
        return

    # If we reach here, the issue is present
    raise AssertionError("Files with same name but different extensions lead to unexpected behavior")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a temporary project directory with the necessary files, configures Sphinx to use the `myst-parser` extension, builds the documentation, and checks if the issue is present. If the issue is not present, it exits with code 0. If the issue is present, it raises an `AssertionError` and prints a stack trace using the provided function.