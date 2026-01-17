To simulate the issue and reproduce the described behavior in a standalone Python file, we will create a minimal Sphinx project environment programmatically. Our script `reproducer.py` will configure Sphinx to use `autodoc` and set `autodoc_typehints` to `none`, then it will try to generate documentation for a simple Python module with type-annotated properties. Afterwards, it will inspect the generated HTML files to check if type hints are present, contrary to the expectation.

```python
import os
import shutil
import subprocess
import sys
from sphinx.application import Sphinx

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

def create_files():
    os.makedirs('test_project', exist_ok=True)
    os.makedirs('test_project/docs', exist_ok=True)
    os.makedirs('test_project/test_module', exist_ok=True)
    with open('test_project/test_module/module.py', 'w') as f:
        f.write("""
class TestClass:
    @property
    def test_property(self) -> str:
        \"\"\"This is a test property.\"\"\"
        return 'test'
""")

    with open('test_project/docs/conf.py', 'w') as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('../test_module'))

project = 'Test Project'
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'none'
html_theme = 'alabaster'
""")

    with open('test_project/docs/index.rst', 'w') as f:
        f.write("""
.. automodule:: module
    :members:
    :undoc-members:
    :show-inheritance:
""")

def run_sphinx():
    try:
        os.chdir('test_project/docs')
        subprocess.run(['sphinx-build', '-b', 'html', '.', '_build/html'], check=True)
    finally:
        os.chdir('../../')

def check_output():
    try:
        with open('test_project/docs/_build/html/module.TestClass.test_property.html') as f:
            contents = f.read()
            if "-> str" in contents:
                raise AssertionError("Type hints are present in the output despite 'autodoc_typehints' being set to 'none'.")
    except FileNotFoundError as e:
        print_stacktrace(e)
        raise AssertionError("Expected documentation file was not generated.") from e

def main():
    create_files()
    run_sphinx()
    check_output()
    print("Issue not present, type hints are correctly excluded from the output.")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    sys.exit(0)
```

Note: This script assumes that Sphinx is already installed in your environment (`pip install sphinx`). Before running the script, ensure you are in an appropriate virtual environment where modifications to the file system are permissible and won't affect your existing projects. The script first sets up a minimal project directory structure and files necessary for Sphinx to run. Then, it runs Sphinx to generate the HTML documentation and finally inspects one of the generated HTML files for the presence of type hints in the output documentation of a property.