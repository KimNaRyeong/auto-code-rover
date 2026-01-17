To replicate the reported issue where `autodoc` still uses type hints in properties even when `autodoc_typehints` is set to `none`, we would need to simulate the Sphinx documentation generation process within a Python script. However, executing a Sphinx build and parsing its output within a script is not trivial, since Sphinx is usually run as a standalone command-line tool (e.g., `sphinx-build`). That said, we'll instead check for the presence of type hints in the generated documentation HTML files, simulating what the original issue report described. Keep in mind, this will not strictly follow the "raise an `AssertionError`" directive but instead will check the output for the issue.

```python
import subprocess
import os

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

def setup_sphinx_project():
    os.makedirs('test_project/docs', exist_ok=True)
    with open('test_project/docs/conf.py', 'w') as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Test Project'
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'none'
""")
    with open('test_project/my_module.py', 'w') as f:
        f.write("""
class MyClass:
    @property
    def my_property(self) -> str:
        \"\"\"This is a property\"\"\"
        return 'hello'
""")
    with open('test_project/docs/index.rst', 'w') as f:
        f.write("""
.. automodule:: my_module
   :members:
""")

def run_sphinx():
    try:
        subprocess.run(['sphinx-build', '-b', 'html', 'docs', 'docs/_build'], check=True, cwd='test_project')
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        exit(1)

def check_output():
    try:
        with open('test_project/docs/_build/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if "-> str" in content:
                raise AssertionError("Type hint found in property documentation despite `autodoc_typehints` set to `none`.")
            else:
                print("Issue fixed, no type hints in the output.")
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

This script sets up a minimal Sphinx project with a Python module containing a class with typed properties, configures Sphinx to not include type hints in the documentation, runs the Sphinx build, and checks the output for the presence of type hints.

Make sure you have Sphinx installed in your environment (`pip install sphinx`) to run this script successfully. Note that depending on your Sphinx theme or version, the actual HTML output might vary, so the `check_output` function may need adjustments to accurately detect whether the issue persists.