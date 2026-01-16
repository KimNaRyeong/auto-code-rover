To adhere strictly to creating a standalone `reproducer.py` without external dependencies and achieving the goal of reproducing the Sphinx documentation issue, I'll provide a Python script that programmatically uses Sphinx to generate documentation and then inspects the generated documentation to ensure there are no type hints present for properties, as expected by the `autodoc_typehints = 'none'` setting. This approach negates the need for BeautifulSoup by directly searching for type hint indicators (like `->`) in the generated HTML files, which are text files.

The script will:
1. Create a minimal Sphinx project with a single Python source file including a class with typed properties.
2. Configure Sphinx to ignore typehints (`autodoc_typehints = 'none'`).
3. Generate the documentation.
4. Inspect the generated HTML for the presence of type hints in the properties description.
5. Assert and report based on findings.

```python
import os
import subprocess
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

def setup_sphinx_project():
    """
    Sets up a minimal Sphinx project with a single Python module.
    """
    os.makedirs('test_project/docs', exist_ok=True)
    os.makedirs('test_project/test_project', exist_ok=True)

    with open('test_project/test_project/test_module.py', 'w') as f:
        f.write(
            '''
class TestClass:
    @property
    def test_property(self) -> str:
        """This is a test property."""
        return "test"
            '''
        )

    with open('test_project/docs/conf.py', 'w') as f:
        f.write(
            '''
import os
import sys
sys.path.insert(0, os.path.abspath('../test_project'))

project = 'Test Project'
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'none'
            '''
        )

    with open('test_project/docs/index.rst', 'w') as f:
        f.write(
            '''
.. automodule:: test_module
    :members:
            '''
        )

def generate_docs():
    """
    Generates Sphinx documentation.
    """
    proc = subprocess.run(['sphinx-build', '-b', 'html', 'docs', 'docs/_build'], cwd='test_project', capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Failed to generate documentation: {proc.stderr}")

def check_for_typehints():
    """
    Checks the generated HTML file for any type hints.
    """
    try:
        with open('test_project/docs/_build/index.html', 'r') as f:
            if '->' in f.read():
                raise AssertionError("Type hints found in properties documentation despite autodoc_typehints being set to 'none'.")
            else:
                print("Success: No type hints found in properties documentation.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def main():
    setup_sphinx_project()
    try:
        generate_docs()
        check_for_typehints()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit code 1 to indicate the issue is present
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Please ensure you have Sphinx installed (`pip install sphinx`) before running this script. Modify the path in the script if your Sphinx project structure differs. The script does not handle the installation of Sphinx or creating a comprehensive Sphinx configuration; it's focused on demonstrating an automation approach for the specific issue described.