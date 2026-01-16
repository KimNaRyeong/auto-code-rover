To create a script that reproduces the described issue, we need to simulate the scenario accurately:

1. **Create a minimal Python project setup**: This includes a simple Python module with type-annotated properties, a small Sphinx documentation setup that tries to document this module, and a configuration (`conf.py`) that sets `autodoc_typehints` to `none`.

2. **Automate documentation build process**: The script will trigger the Sphinx build process to generate HTML documentation.

3. **Verify the output for type hints**: The script should then check the generated HTML files for the presence of type hints for properties, which should not be there as per the expected behavior described.

4. **Raise an AssertionError if the issue is present**: If type hints are found, the script will raise an assertion error.

Below is the standalone Python file, `reproducer.py`, designed to achieve this:

```python
import subprocess
import os
import shutil
from typing import List

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

def create_files():
    os.makedirs("project/docs", exist_ok=True)
    os.makedirs("project/my_module", exist_ok=True)

    with open("project/my_module/__init__.py", "w") as f:
        f.write('''
class MyModel:
    @property
    def my_property(self) -> str:
        """This is my property."""
        return 'hello' 
''')

    with open("project/docs/conf.py", "w") as f:
        f.write('''
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Test Project'
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'none'
html_theme = 'alabaster'
''')

    with open("project/docs/index.rst", "w") as f:
        f.write('''
Welcome to Test Project's documentation!
========================================

.. automodule:: my_module
    :members:
    :private-members:
    :show-inheritance:
''')

def build_docs() -> List[str]:
    result = subprocess.run(["sphinx-build", "-b", "html", "docs", "build"], cwd="project", capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Sphinx documentation build failed.")

    with open("project/build/index.html", "r") as f:
        return f.readlines()

def check_for_typehints(doc_lines: List[str]):
    for line in doc_lines:
        if "-> str" in line:
            raise AssertionError("Type hint found in the output despite 'autodoc_typehints' being set to 'none'.")

try:
    create_files()
    doc_lines = build_docs()
    check_for_typehints(doc_lines)
    print("No type hints found in the properties documentation. Issue resolved or not present.")
except Exception as e:
    print_stacktrace(e)
```

**Important**: Before running this script, ensure you have Sphinx installed (`pip install sphinx`) in your environment and your working directory is set up where you want this test project and documentation to be created and built. This script is designed to be self-contained, ensuring it cleans up by not leaving permanent changes in your environment (you might want to remove the `project` directory manually after testing).