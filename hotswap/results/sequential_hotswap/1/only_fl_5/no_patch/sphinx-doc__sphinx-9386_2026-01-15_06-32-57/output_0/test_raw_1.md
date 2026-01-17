Given the specific requirements and aiming to adhere strictly to the prompt for generating a standalone Python script that raises an `AssertionError` when type hints are present in property documentation despite setting `autodoc_typehints` to `none`, we suggest the following approach:

This script will:
1. Programmatically create the necessary Sphinx project files (configuration, Python module with a documented property, and index file).
2. Run the Sphinx build process within the Python environment.
3. Scrape the generated HTML for the presence of type hints in the property documentation.
4. Raise an `AssertionError` if type hints are found, adhering to the given requirement for indicating the presence of the issue.

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
    os.makedirs('docs', exist_ok=True)
    with open('conf.py', 'w') as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'Test Project'
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'none'
""")
    with open('my_module.py', 'w') as f:
        f.write("""
class MyClass:
    @property
    def my_property(self) -> str:
        \"\"\"This is a property\"\"\"
        return 'hello'
""")
    with open('index.rst', 'w') as f:
        f.write("""
.. automodule:: my_module
   :members:
""")

def run_sphinx():
    try:
        subprocess.run(['sphinx-build', '-b', 'html', '.', '_build'], check=True)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        exit(1)

def check_output():
    try:
        with open('_build/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if "-> str" in content:
                raise AssertionError("Type hint found in property documentation despite `autodoc_typehints` set to `none`.")
            else:
                print("No type hints found in the documentation. The issue is not present.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

def main():
    setup_sphinx_project()
    run_sphinx()
    check_output()

if __name__ == '__main__':
    main()
```

Keep in mind:
- This test assumes that running `sphinx-build` directly from within the script is possible in your environment and that Sphinx is properly installed.
- The actual HTML output might vary with different versions of Sphinx and its themes or extensions, so the check in `check_output()` may require adjustments for different Sphinx configurations or setups.
- Given the conditions for error reporting mentioned in your request, this script will explicitly look for the "-> str" string in the generated HTML, which corresponds to a type hint as evidence of the issue. Adjustments might be needed depending on the exact output Sphinx generates for your project configuration.