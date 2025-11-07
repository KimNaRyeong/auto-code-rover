Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
import os
import sys
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
    # Create a temporary directory for the Sphinx project
    temp_dir = "temp_sphinx_project"
    os.makedirs(temp_dir, exist_ok=True)

    # Create the directory structure
    os.makedirs(os.path.join(temp_dir, "source", "document", "downloads"), exist_ok=True)
    with open(os.path.join(temp_dir, "source", "document", "downloads", "archive.zip"), "w") as f:
        f.write("")

    # Create the index.rst file
    with open(os.path.join(temp_dir, "source", "document", "index.rst"), "w") as f:
        f.write("""
:download:`downloads/archive.zip`
:download:`/document/downloads/archive.zip`
:download:`../document/downloads/archive.zip`
""")

    # Create the conf.py file
    with open(os.path.join(temp_dir, "conf.py"), "w") as f:
        f.write("extensions = ['sphinx.ext.graphviz', 'sphinx.ext.ifconfig']\n")
        f.write("master_doc = 'index'\n")
        f.write("html_static_path = ['_static']\n")

    # Build the Sphinx project
    app = Sphinx(temp_dir, temp_dir, os.path.join(temp_dir, "build"), os.path.join(temp_dir, "_static"))
    app.build()

    # Check if the issue is present
    build_dir = os.path.join(temp_dir, "build", "_downloads")
    files = os.listdir(build_dir)
    assert len(files) == 1, f"Expected 1 file, got {len(files)}: {files}"
    print("Issue not present!")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script creates a temporary Sphinx project with the specified directory structure and content, builds the project, and checks if the issue is present by verifying that only one file is generated in the `_downloads` directory. If the issue is present, it raises an `AssertionError` with a stack trace of the issue.