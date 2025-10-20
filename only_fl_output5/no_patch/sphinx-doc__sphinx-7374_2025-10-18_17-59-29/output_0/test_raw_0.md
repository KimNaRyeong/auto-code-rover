To simulate a reproduction of the issue described, we'll create a minimal Sphinx project environment programmatically. However, please note that this script assumes you have Sphinx and `nbsphinx` installed in your environment where you run this script. The script will dynamically create a minimal Sphinx project with a Python file and an RST file documenting a function. It will then build the documentation and check if the generated HTML anchor uses underscores or dashes for Python function names.

```python
import os
import subprocess
import shutil
from bs4 import BeautifulSoup  # BeautifulSoup is used for parsing HTML

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
    # check for sphinx-build and nbsphinx installation
    try:
        subprocess.run(["sphinx-build", "--version"], check=True, stdout=subprocess.PIPE)
        import nbsphinx  # noqa: F401
    except Exception as e:
        print_stacktrace(e)
        raise RuntimeError("Sphinx or nbsphinx is not installed. Please install before proceeding.")

    # Create minimal Sphinx project structure
    os.makedirs("src", exist_ok=True)
    with open("src/example_python_function.py", "w") as f:
        f.write("""
def example_python_function(foo):
    \"\"\"Some function.\"\"\"
    pass
""")

    with open("src/index.rst", "w") as f:
        f.write("""
.. py:function:: example_python_function(foo)

    Some function.
""")

    os.makedirs("_build", exist_ok=True)

def build_docs():
    cmd = ["sphinx-build", "-b", "html", "src", "_build/html"]
    subprocess.run(cmd, check=True)

def check_anchor():
    with open("_build/html/index.html", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        expected_id = "example-python-function"
        anchor = soup.find(id=expected_id)
        if not anchor:
            raise AssertionError(f"Anchor with ID {expected_id} not found. The issue is present.")

try:
    setup_sphinx_project()
    build_docs()
    check_anchor()
    print("The issue is fixed. Exiting with code 0.")
except Exception as e:
    print_stacktrace(e)
    exit(1)
```

Please make sure to have Sphinx, `nbsphinx`, and BeautifulSoup installed in your Python environment (`pip install sphinx nbsphinx beautifulsoup4`) before running this script. The script will generate a minimal project structure, build the documentation, and then parse the resulting HTML file to check for the presence or absence of the issue. If the function's anchor uses dashes instead of underscores, it will recognize the issue as fixed. Otherwise, it will raise an `AssertionError` indicating the issue is present.