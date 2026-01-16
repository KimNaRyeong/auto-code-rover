Below is a Python script named `reproducer.py` designed to reproduce the issue described regarding the change in Python domain IDs in generated documentation. This script programmatically generates a minimal Sphinx project with a single Python function documented in reStructuredText format. It builds the documentation, then examines the generated HTML to check if the anchor link for the Python function contains dashes instead of underscores, in line with the issue provided.

This specific reproducer is a simplified demonstration and might need adjustments to fit into various environments or versions of Sphinx and its extensions.

```python
import os
import subprocess
import sys
import shutil

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def setup_sphinx_project():
    os.mkdir("test_sphinx")
    os.chdir("test_sphinx")
    os.mkdir("_static")
    os.mkdir("_templates")
    with open("conf.py", "w") as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'Test Project'
master_doc = 'index'
html_theme = 'alabaster'
        """)
    with open("index.rst", "w") as f:
        f.write("""
Welcome to Test Project's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Functions
---------

.. py:function:: example_python_function(foo)

    Some function.
""")
    print("Sphinx project set up.")


def build_sphinx():
    subprocess.run(["sphinx-build", ".", "_build/html"], check=True)
    print("Sphinx build completed.")


def check_documentation():
    with open("_build/html/index.html", "r") as f:
        contents = f.read()
        expected_fragment = "example-python-function"
        assert expected_fragment in contents, "The expected anchor format with dashes is not present in the documentation."


def main():
    try:
        setup_sphinx_project()
        build_sphinx()
        check_documentation()
        print("Success: The issue is fixed.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        # Cleanup
        os.chdir("..")
        shutil.rmtree("test_sphinx", ignore_errors=True)

if __name__ == "__main__":
    main()
```

Note: Before running this script, ensure Sphinx is installed (`pip install sphinx`) and you are executing the script in an environment where it's safe to create and delete directories. This script creates a new directory `test_sphinx`, generates a minimal Sphinx documentation project inside it, builds the documentation, checks for the anchor format, and then cleans up by removing the directory. This automates the process of detecting the described issue with Python domain IDs changes.