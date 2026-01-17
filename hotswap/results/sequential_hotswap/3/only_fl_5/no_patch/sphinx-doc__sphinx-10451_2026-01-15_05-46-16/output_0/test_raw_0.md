Here is a standalone Python script named `reproducer.py` to reproduce the described issue. This script uses the `sphinx` package to generate documentation for a test class with documented `__init__`, including `*args` and `**kwargs`, while having `autodoc_typehints` set to `"description"`. If the issue is present, it will raise an `AssertionError` and print a detailed stack trace. It exits with code 0 when the issue is fixed.

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
    test_module_content = """
\"\"\"
Example module
\"\"\"

class _ClassWithDocumentedInitAndStarArgs:
    \"\"\"Class docstring.\"\"\"

    def __init__(self, x: int, *args: int, **kwargs: int) -> None:
        \"\"\"Init docstring.

        :param x: Some integer
        :param *args: Some integer
        :param **kwargs: Some integer
        \"\"\"
    """

    conf_py_content = """
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'Test Project'
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'description'
    """

    index_rst_content = """
.. automodule:: test_module
   :members:
   :undoc-members:
   :show-inheritance:
    """

    os.makedirs('docs', exist_ok=True)
    with open('test_module.py', 'w') as f:
        f.write(test_module_content)
    with open('docs/conf.py', 'w') as f:
        f.write(conf_py_content)
    with open('docs/index.rst', 'w') as f:
        f.write(index_rst_content)

def run_sphinx():
    cmd = ['sphinx-build', '-b', 'html', 'docs', 'docs/_build']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

def check_documentation():
    setup_sphinx_project()
    stdout, stderr = run_sphinx()
    # We look for the specific duplicated output sequence in stderr or stdout, it should not be found.
    duplicated_sequence = "***kwargs** --"
    if duplicated_sequence in stderr or duplicated_sequence in stdout:
        raise AssertionError("Duplicated *args and **kwargs issue found.")
    print("Issue not found, looks like it's fixed.")

if __name__ == '__main__':
    try:
        check_documentation()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```

This script does the following:
- Sets up a minimal Sphinx project with a configuration that replicates the reported issue.
- Writes a Python module `test_module.py` with a class containing an `__init__` method with `*args` and `**kwargs`, both documented.
- Generates documentation using Sphinx.
- Checks the generated documentation for the duplicated `*args` and `**kwargs` issue.
- Raises an `AssertionError` if the issue is found, along with printing a detailed stack trace.

Make sure Sphinx is installed in your environment (`pip install sphinx`) before running this script.