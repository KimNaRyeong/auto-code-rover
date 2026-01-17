Creating a standalone Python script to reproduce this specific Sphinx documentation generation issue is slightly unconventional, given Sphinx's nature of requiring configuration files (`conf.py`), source files (`.rst` or `.py` with docstrings), and a specific project structure. However, we can create a Python script that programmatically generates the necessary files, runs Sphinx to generate the HTML documentation, and checks the output for type hints against the expected behavior based on the issue description. Please note, this approach will require some simplifications and assumptions about the project structure described in the issue.

```python
"""
reproducer.py

A script to reproduce a Sphinx autodoc typehints issue.
"""

import os
import subprocess
import sys


def create_sphinx_project():
    """Creates a minimal Sphinx project setup with a single Python module and conf.py file."""
    os.makedirs("test_project/docs", exist_ok=True)
    os.makedirs("test_project/package", exist_ok=True)

    # Python module with a property having type hint
    module_content = """\
class MyClass:
    @property
    def my_property(self) -> str:
        \"\"\"This is a property.\"\"\"
        return 'hello'
"""

    # Sphinx configuration
    conf_content = """\
import os
import sys
sys.path.insert(0, os.path.abspath('../package'))

project = 'Sphinx Type Hint Test'
extensions = ['sphinx.ext.autodoc']
html_theme = 'alabaster'
autodoc_typehints = 'none'
"""

    # Write the files
    with open("test_project/package/module.py", "w") as module_file:
        module_file.write(module_content)

    with open("test_project/docs/conf.py", "w") as conf_file:
        conf_file.write(conf_content)

    # Create an index file
    with open("test_project/docs/index.rst", "w") as index_file:
        index_file.write(".. automodule:: module\n   :members:\n")


def run_sphinx():
    """Runs Sphinx to generate HTML documentation."""
    subprocess.run(["sphinx-build", "-b", "html", "docs", "_build/html"], cwd="test_project", check=True)


def check_output():
    """Checks the generated index.html for the presence of type hints."""
    with open("test_project/_build/html/index.html", "r") as html_file:
        contents = html_file.read()
    assert "str" not in contents, "Type hints were found in the output despite autodoc_typehints being set to 'none'."


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


def main():
    try:
        create_sphinx_project()
        run_sphinx()
        check_output()
        print("Success: No issue found.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

This script does the following:
- Creates a minimal Sphinx project with a single Python module that includes a property with a type hint.
- Configures Sphinx to not include type hints in the output by setting `autodoc_typehints` to `'none'` in the `conf.py`.
- Runs Sphinx to generate HTML documentation for the project.
- Checks the generated HTML documentation for the presence of the type hint that should have been excluded.
- Raises an `AssertionError` if the type hint is present, indicating the issue is present, and prints a stack trace. 

Make sure you have Sphinx installed in your environment (`pip install sphinx`) before running this script.