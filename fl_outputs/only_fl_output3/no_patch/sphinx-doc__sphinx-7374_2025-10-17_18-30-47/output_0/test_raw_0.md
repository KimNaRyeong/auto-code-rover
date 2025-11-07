```python
import subprocess
import os
import sys

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

def test_python_function_link_generation():
    # Path to the Sphinx project's root directory
    sphinx_project_root = os.getcwd()

    # Create a minimal Sphinx configuration and a Python file to document
    os.makedirs(os.path.join(sphinx_project_root, "docs"), exist_ok=True)
    os.makedirs(os.path.join(sphinx_project_root, "src"), exist_ok=True)

    conf_py = """\
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))
project = 'TestProject'
master_doc = 'index'
extensions = ['sphinx.ext.autodoc']
"""

    index_rst = """\
.. py:function:: example_python_function(foo)
   :module: my_module

   This is a sample function with underscores in its name.
"""

    my_module_py = """\
def example_python_function(foo):
    \"\"\"This is a sample function with underscores in its name.\"\"\"
    pass
"""

    with open(os.path.join(sphinx_project_root, "docs", "conf.py"), "w") as f:
        f.write(conf_py)

    with open(os.path.join(sphinx_project_root, "docs", "index.rst"), "w") as f:
        f.write(index_rst)

    with open(os.path.join(sphinx_project_root, "src", "my_module.py"), "w") as f:
        f.write(my_module_py)

    # Build the documentation
    result = subprocess.run(["sphinx-build", "-b", "html", "docs", "build/html"], capture_output=True, text=True)

    # Check if the generated HTML file contains the expected anchor link
    try:
        with open("build/html/index.html", "r") as f:
            contents = f.read()
            assert "example_python_function" in contents, "Anchor with underscores not found."
            assert "example-python-function" not in contents, "Anchor with dashes detected."
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Test passed: The issue is fixed.")
        sys.exit(0)

if __name__ == "__main__":
    test_python_function_link_generation()
``` 

This script automates the process of checking for the mentioned issue in the generation of anchor links for Python functions documented using Sphinx. It dynamically creates a minimal Sphinx project with a Python module and a function whose documentation includes an anchor. It then builds that documentation and searches the generated HTML file for the presence of an anchor with underscores versus dashes in its identifier, raising an `AssertionError` if the issue is present (i.e., if it finds the anchor with dashes or fails to find the anchor with underscores). It uses the provided `print_stacktrace` function to print detailed information about where and why the failure occurred if the check fails.