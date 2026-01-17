Given the issue description, to reproduce it with a standalone Python script (`reproducer.py`), we'll simulate the scenario as described, focusing on generating Sphinx documentation that should not include type hints for properties but does, because of the reported bug.

This example assumes you have a Sphinx project set up with at least one Python module that includes properties with type hints. The script will:

1. Create a temporary Sphinx project (if not existing).
2. Generate documentation for a Python module with properties that include type hints.
3. Examine the generated HTML files for evidence of type hints where they should not be.

To clarify, this script won't fully automate the setup of a new Sphinx project or the installation of Sphinx itself. Make sure Sphinx is installed, and you have a basic understanding of how to set it up.

```python
import subprocess
import os
import tempfile
import shutil

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
    # Simulating setup of a Sphinx project
    src_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(src_dir, 'docs'))
    with open(os.path.join(src_dir, 'conf.py'), 'w') as f_conf:
        f_conf.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'none'
""")
    with open(os.path.join(src_dir, 'test_module.py'), 'w') as f_module:
        f_module.write("""
class TestClass:
    @property
    def my_property(self) -> str:
        '''This is a property with a type hint that should not appear in the generated docs.'''
        return 'hello'
""")
    shutil.copyfile('reproducer.py', os.path.join(src_dir, 'docs', 'reproducer.py'))
    return src_dir

def generate_docs(src_dir):
    # Generate HTML documentation
    cwd = os.getcwd()
    os.chdir(os.path.join(src_dir, 'docs'))
    subprocess.call(['sphinx-apidoc', '-o', '.', '..', '-f'])
    subprocess.call(['make', 'html'])
    os.chdir(cwd)

def verify_docs(src_dir):
    html_path = os.path.join(src_dir, 'docs', '_build', 'html', 'test_module.TestClass.html')
    if not os.path.isfile(html_path):
        raise AssertionError("Documentation file not generated.")
    with open(html_path, 'r') as f:
        content = f.read()
        if "-> str" in content:
            raise AssertionError("Type hint found in generated docs despite autodoc_typehints being set to 'none'.")

def main():
    try:
        src_dir = setup_sphinx_project()
        generate_docs(src_dir)
        verify_docs(src_dir)
        print("Documentation generated correctly, no type hints found.")
    except Exception as e:
        print_stacktrace(e)
    finally:
        shutil.rmtree(src_dir)

if __name__ == "__main__":
    main()
```

This script aims to simulate the setup and verification as closely as possible within the constraints of a script without an actual Sphinx project setup or a file to download. It is, however, a conceptual approach; in a real scenario, you would have an existing Sphinx project, and the `reproducer.py` script would need to adapt to that context.