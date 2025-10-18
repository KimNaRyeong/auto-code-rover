Creating a standalone Python script to reproduce the specific issue reported with Sphinx, involving the duplication of files referred in various ways, requires understanding of both the Sphinx build system and Python's filesystem manipulations. The script below aims to mimic the documentation project structure briefly, invoke a Sphinx build, and check for duplicates as described in the issue.

Given the initial setup of the problem, the following `reproducer.py` script has been crafted. It is important to note that due to the complex nature of Sphinx interaction and filesystem checks, simplifications were made to ensure clarity and directness of the reproduction attempt. The script prepares a simple Sphinx project, runs a Sphinx build, and then checks the build output for the unexpected duplicates. 

Ensure you have Sphinx installed in your Python environment before running this script.

```python
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

def create_sphinx_project():
    project_dir = os.path.join(os.getcwd(), "test_sphinx_project")
    source_dir = os.path.join(project_dir, "source")
    build_dir = os.path.join(project_dir, "build")
    shutil.rmtree(project_dir, ignore_errors=True)
    os.makedirs(os.path.join(source_dir, "document", "downloads"), exist_ok=True)
    
    conf_py_content = """
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = []
master_doc = 'index'
project = 'Test Project'
"""

    index_rst_content = """
.. _test-project:

Test Project
============

References to the same file in different ways:

.. download:: downloads/archive.zip

.. download:: /document/downloads/archive.zip

.. download:: ../document/downloads/archive.zip
"""

    with open(os.path.join(source_dir, 'conf.py'), 'w') as conf_file:
        conf_file.write(conf_py_content)
    
    with open(os.path.join(source_dir, 'index.rst'), 'w') as index_file:
        index_file.write(index_rst_content)
    
    with open(os.path.join(source_dir, "document", "downloads", "archive.zip"), 'wb') as zip_file:
        zip_file.write(b"Dummy content for zip file.")
    
    return project_dir, build_dir

def run_sphinx_build(source_dir, build_dir):
    subprocess.check_call(['sphinx-build', '-b', 'html', source_dir, build_dir])

def check_for_duplicates(build_dir):
    downloads_path = os.path.join(build_dir, '_downloads')
    files = os.listdir(downloads_path)
    if len(files) > 1:
        raise AssertionError("Duplicate files found: {}".format(files))

try:
    project_dir, build_dir = create_sphinx_project()
    run_sphinx_build(os.path.join(project_dir, "source"), build_dir)
    check_for_duplicates(build_dir)
    print("Test passed: No duplicate files found.")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

finally:
    # Optional: Clean up the project directory
    # shutil.rmtree(project_dir, ignore_errors=True)
    pass
```

This script includes:

- Setup of a simple Sphinx project with a `conf.py` and `index.rst` that references the same file three different ways.
- Execution of the Sphinx build process.
- Validation to ensure only a single instance of the referenced file exists in the `_downloads` directory after the build.
- Cleanup of the generated project directory to avoid clutter (optional and currently commented out).

Before execution, ensure Sphinx (`sphinx-build`) is available in your environment's `PATH`. This script should be executed from within an environment where Sphinx is installed (e.g., after running `pip install sphinx`). 

Adjustments may be necessary to cater to different environments or Sphinx versions, especially considering path handling on operating systems other than Linux/Unix.