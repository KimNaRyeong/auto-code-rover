Creating a standalone Python script to reproduce the described issue directly involves interfacing with Sphinx. Given the previous attempt where `sphinx-build` was not found, it's important to ensure that Sphinx is correctly installed and accessible in the environment where this script will run. This script assumes that Sphinx is installed and correctly set up. If it's not found, it suggests a potential environment configuration issue that must be resolved separately (e.g., ensuring Sphinx is installed and the environment where Python is running has access to the `sphinx-build` command).

Given these conditions, I'll adjust the initial approach to include a more explicit environment setup check for Sphinx and then proceed with the original plan to simulate the documentation building process and inspect the generated output for the anchor format issue.

```python
import subprocess
import sys
from pathlib import Path

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

def check_sphinx_installation():
    try:
        subprocess.check_output(['sphinx-build', '--version'])
    except FileNotFoundError:
        print("sphinx-build command not found. Please ensure Sphinx is installed and available in your PATH.", file=sys.stderr)
        exit(1)

def setup_sphinx_project():
    project_dir = 'sphinx_test_project'
    Path(project_dir).mkdir(exist_ok=True)
    conf_py = """project = 'Sphinx Anchor Test'
master_doc = 'index'
html_theme = 'alabaster'
"""
    index_rst = """.. py:function:: example_python_function(foo)
   :noindex:

   Some function that should generate a URL fragment.
"""

    Path(f'{project_dir}/conf.py').write_text(conf_py)
    Path(f'{project_dir}/index.rst').write_text(index_rst)

    return project_dir

def build_and_check_sphinx_project(project_dir):
    try:
        subprocess.run(['sphinx-build', '-b', 'html', project_dir, f'{project_dir}/_build/html'], check=True, capture_output=True)
        html_output = Path(f"{project_dir}/_build/html/index.html").read_text()
        expected_anchor = "example-python-function"
        assert expected_anchor in html_output, f"Anchor '{expected_anchor}' not found in HTML output."
        print("Success: Anchor format with dashes is used.")
    except subprocess.CalledProcessError as e:
        print("Failed to build Sphinx documentation.", file=sys.stderr)
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    check_sphinx_installation()
    project_dir = setup_sphinx_project()
    build_and_check_sphinx_project(project_dir)
```

### Notes:

- This script first checks if Sphinx is installed and available in the environment by attempting to get the version of `sphinx-build`. If `sphinx-build` is not found, it will exit with an error message prompting to ensure Sphinx is installed.
- It sets up a minimal Sphinx project directory with a basic `conf.py` and `index.rst` file which attempts to document a Python function. This mimics the scenario described in the issue.
- The script then builds the Sphinx documentation and checks the generated HTML for the presence of an anchor with dashes (as expected after the breaking change). If the anchor with dashes (`example-python-function`) is found, it prints a success message. If there's an error during the build or the assertion fails (e.g., the anchor does not match the expected format), it will print a stack trace.

Please ensure Sphinx is installed in your environment. If you're using a virtual environment, activate it and install Sphinx via pip before running this script:

```
pip install sphinx
```