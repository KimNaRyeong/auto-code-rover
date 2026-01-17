Below is a standalone Python script named `reproducer.py`. This script dynamically generates a Sphinx project, including a file that exhibits the bug described. As requested, the script attempts to build the project using Sphinx. If the generated output contains the issue (in this case, a broken reference), an `AssertionError` will be raised, and a stack trace of the issue will be printed. If the issue does not occur (thereby indicating it has been fixed), the script exits with code 0 (success).

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
    project_root = 'sphinx_rubric_issue'
    if not os.path.exists(project_root):
        os.makedirs(project_root)
    
    # Creating minimal Sphinx configuration
    conf_py = f"""
import sys, os

project = 'Sphinx Rubric Issue'
extensions = []
master_doc = 'index'
"""
    index_rst = """
.. _reference:

.. rubric:: This rubric will be a ``broken`` reference


Let's call the :ref:`reference`
"""
    
    with open(os.path.join(project_root, 'conf.py'), 'w') as f:
        f.write(conf_py)
    
    with open(os.path.join(project_root, 'index.rst'), 'w') as f:
        f.write(index_rst)

    return project_root

def build_sphinx_project(project_root):
    build_cmd = ['sphinx-build', '-M', 'html', project_root, os.path.join(project_root, '_build')]
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Sphinx build failed: {result.stderr}")

    # Assuming Sphinx HTML output
    with open(os.path.join(project_root, '_build', 'html', 'index.html'), 'r') as f:
        content = f.read()
        # Checking if the issue is present
        if "This rubric will be a <code>broken</code> reference" not in content:
            raise AssertionError("The reference is broken!")

try:
    project_root = setup_sphinx_project()
    build_sphinx_project(project_root)

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue not found. Exiting with code 0.")
    sys.exit(0)
```

To use this script:

1. Ensure Python 3 and Sphinx (v3.4.1 to match the environment mentioned) are installed in your environment.
2. Place `reproducer.py` at the root of your intended project directory.
3. Run the script using `python3 reproducer.py`.

This script will:

- Create a temporary Sphinx project with a configuration (`conf.py`) and documentation source file (`index.rst`) matching the description of the issue.
- Attempt to build the project with Sphinx.
- If the problematic output is detected in the built `index.html` file (i.e., the quoted text in the rubric directive causing a broken reference), it raises an `AssertionError`.
- The script captures and prints a stack trace if the assertion fails, thus demonstrating where the issue might be originating in the broader context of the script's execution.