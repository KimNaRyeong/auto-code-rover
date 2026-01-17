Below is a standalone Python script named `reproducer.py`. This script attempts to use Sphinx to generate documentation for a specified class and checks if the documented `*args` and `**kwargs` are duplicated in the output, as described in the issue. It simulates the environment by creating a temporary directory, writing a Python module with the given class, and a Sphinx project to document it. Then, it analyses the generated `index.html` to see if the issue occurs.

Please ensure Sphinx is installed in your environment (`pip install sphinx`) before running this script.

```python
import subprocess
import os
from tempfile import TemporaryDirectory
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

# Prepare a small python file to be documented
python_module_content = """
class _ClassWithDocumentedInitAndStarArgs:
    \"\"\"Class docstring.\"\"\"

    def __init__(self, x: int, *args: int, **kwargs: int) -> None:
        \"\"\"Init docstring.

        :param x: Some integer
        :param *args: Some integers
        :param **kwargs: Some integers
        \"\"\"
"""

conf_py_content = """
# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Test Project'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
]

autodoc_typehints = "description"
"""

index_rst_content = """
.. automodule:: test_module
   :members:
   :undoc-members:
   :show-inheritance:
"""

try:
    with TemporaryDirectory() as temp_dir:
        # Create a test module
        module_path = os.path.join(temp_dir, "test_module.py")
        with open(module_path, "w") as module_file:
            module_file.write(python_module_content)

        # Setup Sphinx source directory
        src_dir = os.path.join(temp_dir, "source")
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "conf.py"), "w") as conf_file:
            conf_file.write(conf_py_content)
        with open(os.path.join(src_dir, "index.rst"), "w") as index_file:
            index_file.write(index_rst_content)

        # Run Sphinx to build the documentation
        build_dir = os.path.join(temp_dir, "build")
        subprocess.run(["sphinx-build", "-b", "html", src_dir, build_dir], check=True)

        # Analyze the output for duplicates
        with open(os.path.join(build_dir, "index.html"), "r") as html_file:
            content = html_file.read()
            occurrences_args = content.count("***args**")
            occurrences_kwargs = content.count("****kwargs**")

            # Assert that there's exactly one occurrence of each
            assert occurrences_args == 1, "Duplicate *args found"
            assert occurrences_kwargs == 1, "Duplicate **kwargs found"

        print("Issue not found. Test passed.")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script creates a temporary Sphinx project with a custom Python module defined by the given class, runs Sphinx to generate the documentation, and checks the `index.html` file for occurrences of the documented `*args` and `**kwargs`. It raises an `AssertionError` if duplicates are found, printing a stack trace that indicates where the issue originated. If the script runs without encountering the issue, it prints "Issue not found. Test passed." and exits gracefully.