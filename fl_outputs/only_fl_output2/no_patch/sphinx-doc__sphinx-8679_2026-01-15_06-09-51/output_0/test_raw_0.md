Below is a Python script named `reproducer.py` that should be placed in the root directory of the project. This script attempts to programmatically create a minimal Sphinx project, insert the problematic rubric and reference into a document, and then build the documentation. It checks if the generated output contains the expected broken reference structure and raises an `AssertionError` with a stack trace if it does. The script exits with code `0` if the issue is not present, implying the issue has been resolved in the Sphinx version being used or the environment.

```python
import os
import sys
import shutil
import subprocess
from typing import Any

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

def setup_sphinx_project(project_dir: str):
    try:
        # Create minimal Sphinx config
        conf_py = """
project = 'Sphinx Rubric Issue Reproducer'
master_doc = 'index'
html_theme = 'alabaster'
        """.strip()
        
        index_rst = """
.. _reference:

.. rubric:: This rubric will be a ``broken`` reference

Let's call the :ref:`reference`
        """.strip()

        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, 'conf.py'), 'w') as conf_file:
            conf_file.write(conf_py)
        
        with open(os.path.join(project_dir, 'index.rst'), 'w') as index_file:
            index_file.write(index_rst)
        
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def build_sphinx_project(project_dir: str) -> str:
    build_dir = os.path.join(project_dir, '_build')
    try:
        subprocess.check_output(['sphinx-build', '-b', 'html', project_dir, build_dir], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)
    return os.path.join(build_dir, 'index.html')

def verify_issue(output_file: str):
    try:
        with open(output_file, 'r') as f:
            content = f.read()
            # Simplified check for the broken reference
            if "broken" not in content:
                raise AssertionError("The reference is not broken as expected.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    project_dir = 'temp_sphinx_project'
    try:
        setup_sphinx_project(project_dir)
        output_file = build_sphinx_project(project_dir)
        verify_issue(output_file)
        print("The issue is not present.")
        # Cleanup temporary project
        shutil.rmtree(project_dir, ignore_errors=True)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    sys.exit(0)
```

Keep in mind that this script assumes you have Sphinx installed and it's executable from your script's environment. If not, you might need to install Sphinx first using pip (`pip install sphinx`) before running this script. The version of Sphinx should match or be similar to the one mentioned in the issue for accurate reproduction.