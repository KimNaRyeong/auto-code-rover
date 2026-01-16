Below is a `reproducer.py` Python script designed to reproduce the described issue. This script depends on Sphinx being installed and correctly set up in your environment. It dynamically creates the Sphinx documentation for a problematic class and analyses the output to verify if the duplication issue of `*args` and `**kwargs` is present. If the issue exists, the script will raise an `AssertionError`, allowing you to see a stack trace with the help of the provided `print_stacktrace` function.

```python
import os
import sys
import subprocess
from sphinx.application import Sphinx

def create_test_files():
    with open('test_module.py', 'w') as f:
        f.write('''
class _ClassWithDocumentedInitAndStarArgs:
    """Class docstring."""

    def __init__(self, x: int, *args: int, **kwargs: int) -> None:
        """Init docstring.

        :param x: Some integer
        :param *args: Some integer
        :param **kwargs: Some integer
        """

''')

    with open('conf.py', 'w') as f:
        f.write('''
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

extensions = [
    'sphinx.ext.autodoc',
]

autodoc_typehints = "description"
''')

    if not os.path.exists('index.rst'):
        with open('index.rst', 'w') as f:
            f.write('''
Welcome to Test Documentation
=============================

.. automodule:: test_module
    :members:
    :undoc-members:
    :special-members:
''')

def build_docs():
    subprocess.call(['sphinx-apidoc', '-o', '.', './test_module.py'], stdout=subprocess.DEVNULL)
    return subprocess.call(['sphinx-build', '-b', 'text', '.', '_build'], stdout=subprocess.DEVNULL)

def verify_output():
    with open('_build/index.txt', 'r') as f:
        contents = f.read()
        return "***args**" in contents and "****kwargs**" in contents and contents.count("***args**") == 1 and contents.count("****kwargs**") == 1

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
        create_test_files()
        result = build_docs()
        if result != 0:
            raise RuntimeError("Documentation build failed.")
        if not verify_output():
            raise AssertionError("Duplicated *args and **kwargs issue with autodoc_typehints is present.")
        print("Issue not found, documentation generated correctly.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Please make sure you have Sphinx installed in your environment (`pip install Sphinx`) and that your current directory is suitable for Sphinx documentation generation. When you run this script (`python3 reproducer.py`), it will:

1. Create a Python module (`test_module.py`) with the class definition causing the issue. 
2. Generate a minimal Sphinx configuration (`conf.py`) that replicates the problem setup.
3. Create an `index.rst` file pointing to the problematic module for documentation.
4. Attempt to build the Sphinx documentation.
5. Check the generated output for duplications of `*args` and `**kwargs`.
6. It will exit with code 0 if no issue is found (i.e., if the issue is fixed in the future). Otherwise, it will raise an `AssertionError`, indicating the problem persists, showing a stack trace for debugging purposes.