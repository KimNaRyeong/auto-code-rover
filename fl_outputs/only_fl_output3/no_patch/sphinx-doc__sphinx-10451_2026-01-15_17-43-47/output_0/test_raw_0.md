To reproduce the issue described, we'll write a Python script named `reproducer.py`. This script will dynamically generate a Sphinx documentation for a sample class with `*args` and `**kwargs` in its `__init__` method, similar to the described scenario. The script then checks the generated documentation for the duplication issue and raises an `AssertionError` if the issue is present or exits cleanly if the issue is fixed.

Here is how you can create `reproducer.py`:

```python
# reproducer.py
import os
import shutil
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

def check_documentation(output_dir):
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "r") as f:
        contents = f.read()
        
    # Look for duplicated args or kwargs pattern
    if contents.count("<dt>args</dt>") > 1 or contents.count("<dt>kwargs</dt>") > 1:
        raise AssertionError("Duplicated *args or **kwargs found in the documentation.")

    if not ("***args** (*int*)" in contents and "****kwargs** (*int*)" in contents):
        raise AssertionError("Expected documentation format for *args or **kwargs not found.")

def generate_sphinx_docs():
    # Define the directories
    docs_source_dir = "docs"
    output_dir = os.path.join(docs_source_dir, "_build")

    if os.path.exists(docs_source_dir):
        shutil.rmtree(docs_source_dir)
    os.makedirs(docs_source_dir)
    
    # Create a simple Sphinx conf.py file
    with open(os.path.join(docs_source_dir, "conf.py"), "w") as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
project = 'TestProject'
extensions = ['sphinx.ext.autodoc']
autodoc_typehints = "description"
""")

    # Create a Python file to document
    with open("test_module.py", "w") as f:
        f.write("""
class _ClassWithDocumentedInitAndStarArgs:
    \"\"\"Class docstring.\"\"\"

    def __init__(self, x: int, *args: int, **kwargs: int) -> None:
        \"\"\"Init docstring.
        
        :param x: Some integer
        :param *args: Some integer
        :param **kwargs: Some integer
        \"\"\"
""")

    # Create an index.rst file
    with open(os.path.join(docs_source_dir, "index.rst"), "w") as f:
        f.write("""
.. automodule:: test_module
   :members:
   :undoc-members:
   :show-inheritance:
""")

    # Execute sphinx-build to generate the docs
    subprocess.check_call(['sphinx-build', '-b', 'html', docs_source_dir, output_dir])
    
    return output_dir

def main():
    try:
        output_dir = generate_sphinx_docs()
        check_documentation(output_dir)
        print("Issue not found, exiting cleanly.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script works by first setting up a basic Sphinx project programmatically, including the creation of a simple Python class with documentation similar to the one described in the issue. The script then uses `sphinx-build` to generate the HTML documentation for this class. Afterward, it checks the generated HTML file for the specific duplication issue. If the issue is present, the script raises an `AssertionError` and prints a stack trace; otherwise, it reports that the issue was not found and exits cleanly.