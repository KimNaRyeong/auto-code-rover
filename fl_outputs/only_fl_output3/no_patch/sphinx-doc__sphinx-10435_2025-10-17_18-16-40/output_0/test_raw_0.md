To devise a standalone Python script capable of reproducing the issue described, we need to interact with a Sphinx project, recreate the issue, and examine the LaTeX output for the unintended spaces. This script will create a minimal Sphinx project with the necessary configuration and files, build the project with LaTeX, and then inspect the resulting `.tex` file for the specific whitespace issue.

Given the nature of the issue, detecting it programmatically involves searching the generated LaTeX file for the problematic space patterns around inline code blocks. This approach assumes that Sphinx and the necessary dependencies are already installed in the environment where this script is executed.

```python
import os
import subprocess
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
    project_dir = 'sphinx_issue_reproducer'
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
    conf_py = """import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'Sphinx Issue Reproducer'
author = 'Author'
version = '1.0'
release = '1.0'
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
latex_elements = {}
latex_documents = [
  (master_doc, 'TestDoc.tex', 'Sphinx Issue Reproducer',
   'Author', 'manual'),
]
"""
    index_rst = """.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

    def foo(1 + 2 + None + "abc"): pass
"""
    with open(os.path.join(project_dir, 'conf.py'), 'w') as f:
        f.write(conf_py)
    with open(os.path.join(project_dir, 'index.rst'), 'w') as f:
        f.write(index_rst)

def build_sphinx_project():
    project_dir = 'sphinx_issue_reproducer'
    subprocess.run(['sphinx-build', '-b', 'latex', project_dir, os.path.join(project_dir, '_build/latex')], check=True)

def check_for_issue():
    tex_file_path = 'sphinx_issue_reproducer/_build/latex/TestDoc.tex'
    with open(tex_file_path, 'r') as f:
        content = f.read()
        if "\\sphinxcode{\\sphinxupquote{" in content:
            raise AssertionError("Whitespaces detected around inline code blocks in LaTeX output.")

def cleanup():
    shutil.rmtree('sphinx_issue_reproducer', ignore_errors=True)

if __name__ == '__main__':
    try:
        setup_sphinx_project()
        build_sphinx_project()
        check_for_issue()
        print("No issue detected. Exiting with code 0.")
    except Exception as e:
        print_stacktrace(e)
        cleanup()
        exit(1)
    cleanup()
    exit(0)
```

Key points about this script:
- It creates a minimal Sphinx project with a configuration (`conf.py`) and a source file (`index.rst`) that includes the described inline code role.
- It runs Sphinx to build the project with a LaTeX output.
- It checks the generated `.tex` file for the specific issue described.
- If the issue is present, it raises an `AssertionError` and prints a stack trace showing where in the script the issue was detected.
- The script ensures cleanup of the project directory whether an issue is found or not.
- It assumes that the `sphinx-build` command is available in the environment's PATH where this script is executed.